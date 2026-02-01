#!/use/bin/python
""" This file contains the classes Chunk and ChunkManager.
It also defines a CHUNK_MANAGER singleton instance.

All coordinates are modeled as pygame.math.Vector2.

There are three types of coordinates:
 - world coordinates
     global coordinates; (0,0) is at world spawn
 - tile coordinates
     "index" of a chunk. The chunk from (0,0) to (32,32) has
     index/tile coordinates (0,0), the chunk next to it is
     identified as (1,0) etc. Each chunk has its own tile coordinate.
 - chunk coordinates
     these can be used inside of a chunk. They are world coordinates, but
     shifted, so that (0,0) lies in the corner of the chunk.

These functions are defined for working with the coordinate systems and converting between them:
 - world_to_tile(world_pos: Vector2) -> Vector2
 - tile_to_world(tile_pos: Vector2) -> Vector2
 - world_to_chunk(world_pos: Vector2, tile_pos: Vector2) -> Vector2
 - chunk_to_world(chunk_pos: Vector2, tile_pos: Vector2) -> Vector2
 - distance_to_chunk_center(pos: Vector2, tile_pos: Vector2) -> float - returns the distance of pos (world coordinates) to the tile's center specified by tile_pos.

"""

import math
import pygame
from pygame.math import Vector2
import numpy as np

from src.simulation_constants import *
import src.noise.noise_engine as noise_engine
from src.biome.biome_placement import get_chunk_biome_map, biome_vectors_to_rgb


### Noise setup
ALTITUDE_NOISE_ENGINE = noise_engine.NoiseEngine(
    seed=ALTITUDE_NOISE_SEED,
    frequency=ALTITUDE_NOISE_FREQUENCY,
    fractal_octaves=ALTITUDE_NOISE_OCTAVES
)
TEMPERATURE_NOISE_ENGINE = noise_engine.NoiseEngine(
    seed=TEMPERATURE_NOISE_SEED,
    frequency=TEMPERATURE_NOISE_FREQUENCY,
    fractal_octaves=TEMPERATURE_NOISE_OCTAVES
)


### Classes Chunk and ChunkManager

class Chunk():
    """ Chunks can be
     - only created (instantiated) which is nothing more than having created this object
     - loaded (aka generated)
    Loading a chunk creates the 8 neighboring Chunk objects if they don't exist already.
    """
    #number_of_objects = 0 # used to count the number of existing chunks and thereby test the unloading
    
    def __init__(self, tile_pos: Vector2):
        """
        params:
         - tile_pos: Vector2 - the index of the chunk (tile_coordinate)
         - chunk_manager: ChunkManager - reference back to the chunk manager that owns this chunk
        """
        self.tile_pos = tile_pos

        self.neighbors = dict() # maps (x,y) to Chunk objects
        self.env_maps = {
            "altitude": None,
            "temperature": None,
            "precipitation": None,
            "biomes": None
        }
        
        self.is_loaded = False
        
        self.surface = pygame.Surface(CHUNK_SIZE)
        self._draw_surface()

        #Chunk.number_of_objects += 1 # count the number of existing chunks

    #def __del__(self):
        #Chunk.number_of_objects -= 1

    def get_corner_points(self) -> list[Vector2]:
        """ returns the four corner points of this chunk, given in world coordinates """
        return [tile_to_world(self.tile_pos + Vector2(i, j)) for i, j in ((0, 0), (0, 1), (1, 0), (1, 1))]

    def load(self):
        if self.is_loaded: return
        self._create_neighbors()
        self.env_maps["altitude"] = ALTITUDE_NOISE_ENGINE.get_noise_height_map(self.tile_pos.x, self.tile_pos.y)
        self._reshape_altitude()
        self.env_maps["temperature"] = TEMPERATURE_NOISE_ENGINE.get_noise_height_map(self.tile_pos.x, self.tile_pos.y)
        # TODO: calculate wind from temperature
        # TODO: calculate precipitation from wind
        self.env_maps["precipitation"] = self.env_maps["temperature"]#np.zeros((int(CHUNK_SIZE.x), int(CHUNK_SIZE.y)), dtype=np.float32)
        self.env_maps["biomes"] = get_chunk_biome_map(self.env_maps["precipitation"], self.env_maps["temperature"])
        # TODO: asset placement
        self.is_loaded = True
        self._draw_surface()

    def unload(self):
        """ unloads the chunk, removes references and "prepares" this chunk to be deleted by garbage collector """
        self.neighbors.clear()
        self.surface = None

    @property
    def position(self):
        return self.tile_pos

    # TODO Change this function so that it properly adds the correct color.
    # Take the biome(s) into consideration.
    def _draw_surface(self):
        """ code that visualizes the state of the chunk (unloaded -> red)
        and the biomes as colors anad the altitude layer as brightness.
        water is set by cutoff and set to blue """
        
        if not self.is_loaded:
            self.surface.fill((60, 40, 40))
            return
        
        a = self.env_maps["altitude"]
        WATER_LEVEL = 0.2 # hard coded for now
        WATER_COLOR = [0.0, 0.1, 0.3]
        water_mask = a <= WATER_LEVEL

        # base colors by biomes
        biome_colors = biome_vectors_to_rgb(self.env_maps["biomes"])
        # set water blue
        biome_colors[water_mask] = np.array(WATER_COLOR)/WATER_LEVEL

        # for now, altitude controls brightness
        colors = biome_colors * a[:, :, np.newaxis]

        # apply to surface
        pygame_colors = np.clip((colors * 255).astype(np.uint8), 0, 255)
        pygame.surfarray.blit_array(self.surface, pygame_colors)

    def _create_neighbors(self):
        for x in (-1,0,1):
          for y in (-1,0,1):
            tile_pos = (self.position.x + x, self.position.y + y)
            if tile_pos in self.neighbors:
                continue
            CHUNK_MANAGER.create_chunk(Vector2(*tile_pos))
            self.neighbors[tile_pos] = CHUNK_MANAGER.chunks[tile_pos]

    def _reshape_altitude(self):
        """ Changes the self.env_maps["altitude"] map to create better looking terrain.
        This function applies a function [0,1] -> [0,1] to make peaks peakier and plateaus plateauier.
        Performance is guaranteed by using numpy's linear interpolation. """
        n = 1001 # 0.001 resolution
        x_lut = np.linspace(0.0, 1.0, n)
        y_lut = np.clip(
            -  0.0016371863
            -  2.219893*x_lut
            + 23.44919786*x_lut**2
            - 67.458179075828*x_lut**3
            + 81.07774578363*x_lut**4
            - 33.86123680241*x_lut**5,
                0, 1
        )
        self.env_maps["altitude"] = \
            (lambda x: np.interp(x, x_lut, y_lut))(
                self.env_maps["altitude"]
            )
            

class ChunkManager():

    def __init__(self):
        self._chunks = dict() # mapping (x, y) in tile_coordinates to Chunk objects

    def update(self, camera_pos: Vector2):
        p = world_to_tile(camera_pos)
        # chunk unloading
        self._unload_chunks_away_from_camera(camera_pos)
        # chunk loading
        self._load_chunks_near_camera(camera_pos)

    def create_chunk(self, tile_pos: Vector2):
        """If there does not exist a chunk at tile_pos, creates one and puts it there."""
        if tuple(tile_pos) in self._chunks:
            return
        self._chunks[tuple(tile_pos)] = Chunk(tile_pos)

    @property
    def chunks(self) -> set[Chunk]:
        return self._chunks

    def _unload_chunks_away_from_camera(self, camera_pos: Vector2):
        for tile_pos in tuple(self._chunks.keys()):
            if distance_to_chunk_center(camera_pos, Vector2(tile_pos[0], tile_pos[1])) >= DISTANCE_FOR_UNLOADING_CHUNKS:
                chunk = self._chunks[tile_pos]
                chunk.unload()
                del self._chunks[tile_pos]

    def _load_chunks_near_camera(self, camera_pos: Vector2):
        camera_tile = world_to_tile(camera_pos)
        # get the tile positions for all chunks in radius of DISTANCE_FOR_LOADING_CHUNKS
        tile_positions = []
        ADDITIONAL_DISTANCE_FOR_SAFETY = 2 # the next step removes tile positions that are too far
        num_chunks_x_dir = math.ceil(DISTANCE_FOR_LOADING_CHUNKS / CHUNK_SIZE.x)+ADDITIONAL_DISTANCE_FOR_SAFETY 
        num_chunks_y_dir = math.ceil(DISTANCE_FOR_LOADING_CHUNKS / CHUNK_SIZE.y)+ADDITIONAL_DISTANCE_FOR_SAFETY 
        for x in range(-num_chunks_x_dir, num_chunks_x_dir):
            for y in range(-num_chunks_y_dir, num_chunks_y_dir):
                chunk_pos = Vector2(x, y) + camera_tile
                if distance_to_chunk_center(camera_pos, chunk_pos) <= DISTANCE_FOR_LOADING_CHUNKS:
                    tile_positions.append(chunk_pos)
        # do the chunk loading
        for p in tile_positions:
            if tuple(p) in self._chunks:
                c = self._chunks[tuple(p)]
            else:
                self._chunks[tuple(p)] = c = Chunk(p)
            c.load() # in case they aren't already


### Coordinate conversion functions

""" world_position gets rounded to get the position of the chunk it is inside of """
def world_to_tile(world_pos: Vector2) -> Vector2:
    return Vector2(int(round(world_pos.x / CHUNK_SIZE.x)), int(round(world_pos.y / CHUNK_SIZE.y)))

def tile_to_world(tile_pos: Vector2) -> Vector2:
    return Vector2(tile_pos.x * CHUNK_SIZE.x, tile_pos.y * CHUNK_SIZE.y)

def world_to_chunk(world_pos: Vector2, tile_pos: Vector2) -> Vector2:
    return tile_to_world(tile_pos) - world_pos

def chunk_to_world(chunk_pos: Vector2, tile_pos: Vector2) -> Vector2:
    return chunk_pos + tile_to_world(tile_pos)

def distance_to_chunk_center(pos: Vector2, tile_pos: Vector2) -> float:
    """ returns the distance of pos (world coordinates) to the tile's center specified by tile_pos. """
    center = tile_to_world(tile_pos) + CHUNK_SIZE / 2
    return pos.distance_to(center)

# instantiate ChunkManager Singleton
CHUNK_MANAGER = ChunkManager()
