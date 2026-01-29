#!/use/bin/python
""" This file contains the classes Chunk and ChunkManager.

The following global variables are defined:
 - CHUNK_SIZE: pygame.math.Vector2 - the size of every chunk
 - DISTANCE_FOR_LOADING_CHUNKS: int - chunks inside this distance are loaded
 - DISTANCE_FOR_UNLOADING_CHUNKS: int - chunks outside this distance are unloaded/deleted
 - CHUNK_MANAGER: ChunkManager - a singleton holding the chunk objects and managing the loading and unloading of chunks

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
 - distance_to_chunk(pos: Vector2, tile_pos: Vector2) -> float - returns the distance of pos (world coordinates) to the tile specified by tile_pos.
    0 means inside or exactly on the border.

"""

import math
import pygame
from pygame.math import Vector2


### Constant variables
CHUNK_SIZE = Vector2(32, 32)
DISTANCE_FOR_LOADING_CHUNKS = 200
DISTANCE_FOR_UNLOADING_CHUNKS = 280
assert(DISTANCE_FOR_LOADING_CHUNKS < DISTANCE_FOR_UNLOADING_CHUNKS)

### Classes Chunk and ChunkManager

class Chunk():
    """ Chunks can be
     - only created (instantiated) which is nothing more than having created this object
     - loaded (aka generated)
    Loading a chunk creates the 8 neighboring Chunk objects if they don't exist already.
    """
    
    def __init__(self, tile_pos: Vector2):
        """
        params:
         - tile_pos: Vector2 - the index of the chunk (tile_coordinate)
         - chunk_manager: ChunkManager - reference back to the chunk manager that owns this chunk
        """
        self.tile_pos = tile_pos

        self.neighbors = dict() # maps (x,y) to Chunk objects

        self.is_loaded = False
        
        self.surface = pygame.Surface(CHUNK_SIZE)
        self._draw_surface()

    def get_corner_points(self) -> list[Vector2]:
        """ returns the four corner points of this chunk, given in world coordinates """
        return [tile_to_world(self.tile_pos + Vector2(i, j)) for i, j in ((0, 0), (0, 1), (1, 0), (1, 1))]

    def load(self):
        if self.is_loaded: return
        self._create_neighbors()
        ... # chunk generation goes here
        self.is_loaded = True
        self._draw_surface()

    @property
    def position(self):
        return self.tile_pos

    # TODO Change this function so that it properly adds the correct color.
    # Take the biome(s) into consideration.
    def _draw_surface(self):
        self.surface.fill((70, 255, 50) if self.is_loaded else (60, 40, 40))

    def _create_neighbors(self):
        for x in (-1,0,1):
          for y in (-1,0,1):
            tile_pos = (self.position.x + x, self.position.y + y)
            if tile_pos in self.neighbors:
                continue
            CHUNK_MANAGER.create_chunk(Vector2(*tile_pos))
            self.neighbors[tile_pos] = CHUNK_MANAGER.chunks[tile_pos]
            

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

    def _unload_chunks_away_from_camera(self, camera_pos):
        for tile_pos in tuple(self._chunks.keys()):
            if distance_to_chunk(camera_pos, tile_pos) >= DISTANCE_FOR_UNLOADING_CHUNKS:
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
                if distance_to_chunk(camera_pos, chunk_pos) <= DISTANCE_FOR_LOADING_CHUNKS:
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

def distance_to_chunk(pos: Vector2, tile_pos: Vector2) -> float:
    """ returns the distance of pos (world coordinates) to the tile specified by tile_pos.
    0 means inside or exactly on the border. """
    ### get corner points
    corner_points = Chunk(tile_pos).get_corner_points()
    ### characterize the position
    x, y = 0, 0
    if all(p.x < pos.x for p in corner_points):
        x = 1
    if all(p.x > pos.x for p in corner_points):
        x = -1
    if all(p.y < pos.y for p in corner_points):
        y = 1
    if all(p.y > pos.y for p in corner_points):
        y = -1
    ### calculate the right distance
    if x == 0 and y == 0: return 0
    if x != 0 and y != 0: return min(pos.distance_to(p) for p in corner_points)
    if x == 0 and y != 0: return min(abs(pos.y - p.y) for p in corner_points)
    if x != 0 and y == 0: return min(abs(pos.x - p.x) for p in corner_points)


# instantiate ChunkManager Singleton
CHUNK_MANAGER = ChunkManager()
