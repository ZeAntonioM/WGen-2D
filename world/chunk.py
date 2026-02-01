# world/chunk.py
import pygame
from pygame.math import Vector2
import settings
from world.utils import tile_to_world # Import from your new utils file

class Chunk:
    def __init__(self, tile_pos: Vector2):
        self.tile_pos = tile_pos
        self.neighbors = dict()
        self.is_loaded = False
        self.surface = pygame.Surface(settings.CHUNK_SIZE)
        self._draw_surface()

    def get_corner_points(self) -> list[Vector2]:
        return [tile_to_world(self.tile_pos + Vector2(i, j)) for i, j in ((0, 0), (0, 1), (1, 0), (1, 1))]

    def load(self):
        if self.is_loaded: return
        self._create_neighbors()
        # Generation logic would go here
        self.is_loaded = True
        self._draw_surface()

    def unload(self):
        self.neighbors.clear()
        self.surface = None

    @property
    def position(self):
        return self.tile_pos

    def _draw_surface(self):
        self.surface.fill((70, 255, 50) if self.is_loaded else (60, 40, 40))

    def _create_neighbors(self):
        # --- CIRCULAR IMPORT FIX ---
        # We import CHUNK_MANAGER here, inside the function, 
        # so it is only loaded when this specific method is called.
        from world.chunk_manager import CHUNK_MANAGER 
        
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                tile_pos = (self.position.x + x, self.position.y + y)
                if tile_pos in self.neighbors:
                    continue
                
                CHUNK_MANAGER.create_chunk(Vector2(*tile_pos))
                self.neighbors[tile_pos] = CHUNK_MANAGER.chunks[tile_pos]