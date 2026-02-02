# world/chunk_manager.py
import math
from pygame.math import Vector2
import settings
from world.chunk import Chunk
from world.utils import world_to_tile, distance_to_chunk_center
from generation.generator import Generator

class ChunkManager:
    def __init__(self, generator: Generator):
        self._chunks = dict()
        self.generator = generator

    def update(self, camera_pos: Vector2):
        self._unload_chunks_away_from_camera(camera_pos)
        self._load_chunks_near_camera(camera_pos)

    def create_chunk(self, tile_pos: Vector2):
        if tuple(tile_pos) in self._chunks:
            return
        self._chunks[tuple(tile_pos)] = Chunk(tile_pos)

    @property
    def chunks(self) -> dict:
        return self._chunks

    def _unload_chunks_away_from_camera(self, camera_pos: Vector2):
        for tile_pos in list(self._chunks.keys()):
            if distance_to_chunk_center(camera_pos, Vector2(tile_pos[0], tile_pos[1])) >= settings.UNLOAD_DISTANCE:
                chunk = self._chunks[tile_pos]
                chunk.unload()
                del self._chunks[tile_pos]

    def _load_chunks_near_camera(self, camera_pos: Vector2):
        camera_tile = world_to_tile(camera_pos)
        tile_positions = []
        ADDITIONAL_DISTANCE = 2 
        
        num_chunks_x = math.ceil(settings.LOAD_DISTANCE / settings.CHUNK_SIZE.x) + ADDITIONAL_DISTANCE 
        num_chunks_y = math.ceil(settings.LOAD_DISTANCE / settings.CHUNK_SIZE.y) + ADDITIONAL_DISTANCE 
        
        for x in range(-num_chunks_x, num_chunks_x):
            for y in range(-num_chunks_y, num_chunks_y):
                chunk_pos = Vector2(x, y) + camera_tile
                if distance_to_chunk_center(camera_pos, chunk_pos) <= settings.LOAD_DISTANCE:
                    tile_positions.append(chunk_pos)
        
        for p in tile_positions:
            if tuple(p) in self._chunks:
                c = self._chunks[tuple(p)]
            else:
                self._chunks[tuple(p)] = c = Chunk(p, self.generator)
            c.load()
