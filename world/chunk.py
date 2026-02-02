import pygame
import numpy as np
from pygame.math import Vector2
import settings
from world.utils import tile_to_world, apply_function_to_map

from generation import noise_engine
from generation.biome_placement import get_chunk_biome_map
from generation.engine_singletons import *

import graphics.visuals as visuals  

class Chunk:
    def __init__(self, tile_pos: Vector2):
        self.tile_pos = tile_pos
        self.neighbors = dict()
        
        self.env_maps = dict()
        
        self.is_loaded = False
        self.surface = pygame.Surface(settings.CHUNK_SIZE)
        self.update_graphics()

    def get_corner_points(self) -> list[Vector2]:
        return [tile_to_world(self.tile_pos + Vector2(i, j)) for i, j in ((0, 0), (0, 1), (1, 0), (1, 1))]

    def load(self):
        if self.is_loaded: return
        self._create_neighbors()
        
        self.env_maps["terrain"] = TERRAIN_ENGINE.get_terrain_map(self.tile_pos.x, self.tile_pos.y)
        
        self.env_maps["temperature"] = TEMPERATURE_NOISE_ENGINE.get_noise_height_map(self.tile_pos.x, self.tile_pos.y)

        self.env_maps["water_level"] = WATER_ENGINE.get_water_level_map(self.tile_pos.x, self.tile_pos.y)
        
        self.env_maps["precipitation"] = CLIMATE_ENGINE.get_precipitation_map(self.tile_pos.x, self.tile_pos.y)
        
        self.env_maps["biomes"] = get_chunk_biome_map(self.env_maps["precipitation"], self.env_maps["temperature"])
        
        self.is_loaded = True
        self.update_graphics()

    def unload(self):
        self.neighbors.clear()
        self.surface = None

    @property
    def position(self):
        return self.tile_pos

    def update_graphics(self, mode="biomes"):
        """
        Asks the visuals module to repaint this chunk's surface.
        """
        visuals.update_chunk_surface(
            surface=self.surface,
            env_maps=self.env_maps,
            is_loaded=self.is_loaded,
            mode=mode
        )

    def _create_neighbors(self):
        from world.chunk_manager import CHUNK_MANAGER
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                tile_pos = (self.position.x + x, self.position.y + y)
                if tile_pos in self.neighbors: continue
                CHUNK_MANAGER.create_chunk(Vector2(*tile_pos))
                self.neighbors[tile_pos] = CHUNK_MANAGER.chunks[tile_pos]
