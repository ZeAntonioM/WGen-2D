import pygame
import numpy as np
from pygame.math import Vector2
import settings
from world.utils import tile_to_world

from generation import noise_engine
from generation.biome_placement import get_chunk_biome_map
from generation.climate_engine import ClimateEngine
from generation.wind_engine import WindEngine

import graphics.visuals as visuals 
from generation.object_engine import ObjectEngine
OBJECT_ENGINE = ObjectEngine(settings.GLOBAL_SEED) 

ALTITUDE_NOISE_ENGINE = noise_engine.NoiseEngine(
    seed=settings.ALTITUDE_NOISE_SEED,
    frequency=settings.ALTITUDE_NOISE_FREQUENCY,
    fractal_octaves=settings.ALTITUDE_NOISE_OCTAVES
)
TEMPERATURE_NOISE_ENGINE = noise_engine.NoiseEngine(
    seed=settings.TEMPERATURE_NOISE_SEED,
    frequency=settings.TEMPERATURE_NOISE_FREQUENCY,
    fractal_octaves=settings.TEMPERATURE_NOISE_OCTAVES
)
WIND_ENGINE = WindEngine(seed=settings.GLOBAL_SEED, scale=settings.WIND_SCALE)
CLIMATE_ENGINE = ClimateEngine(ALTITUDE_NOISE_ENGINE, WIND_ENGINE)

class Chunk:
    def __init__(self, tile_pos: Vector2):
        self.tile_pos = tile_pos
        self.neighbors = dict()
        
        self.env_maps = {
            "altitude": None,
            "temperature": None,
            "precipitation": None,
            "biomes": None,
            "water_cutoff": None 
        }
        
        self.is_loaded = False
        self.surface = pygame.Surface(settings.CHUNK_SIZE)
        self.update_graphics()

    def get_corner_points(self) -> list[Vector2]:
        return [tile_to_world(self.tile_pos + Vector2(i, j)) for i, j in ((0, 0), (0, 1), (1, 0), (1, 1))]

    def load(self):
        if self.is_loaded: return
        self._create_neighbors()
        
        self.env_maps["altitude"] = ALTITUDE_NOISE_ENGINE.get_noise_height_map(self.tile_pos.x, self.tile_pos.y)
        self._reshape_altitude()
        
        self.env_maps["temperature"] = TEMPERATURE_NOISE_ENGINE.get_noise_height_map(self.tile_pos.x, self.tile_pos.y)
        
        self.env_maps["precipitation"] = CLIMATE_ENGINE.get_precipitation_map(self.tile_pos.x, self.tile_pos.y)
        
        self.env_maps["biomes"] = get_chunk_biome_map(self.env_maps["precipitation"], self.env_maps["temperature"])

        self.env_maps["biomes"] = get_chunk_biome_map(self.env_maps["precipitation"], self.env_maps["temperature"])


        self.env_maps["objects"] = OBJECT_ENGINE.generate_object_map(
            self.tile_pos.x, 
            self.tile_pos.y, 
            self.env_maps["biomes"],
            self.env_maps["altitude"],  
            settings.SEA_LEVEL
        )


        self._adjust_water_cutoff()
        
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

    def _reshape_altitude(self):
        n = 1001 
        x_lut = np.linspace(0.0, 1.0, n)
        y_lut = np.clip(
            - 0.0016371863 - 2.219893 * x_lut + 23.44919786 * x_lut**2
            - 67.458179075828 * x_lut**3 + 81.07774578363 * x_lut**4
            - 33.86123680241 * x_lut**5, 0, 1
        )
        self.env_maps["altitude"] = np.interp(self.env_maps["altitude"], x_lut, y_lut)

    def _adjust_water_cutoff(self):
        """ 
        Applies a polynomial function to set the water_cutoff env_map, depending on the precipitation.
        (Friend's New Method)
        """
        n = 1001 
        x_lut = np.linspace(0.0, 1.0, n)
        y_lut = np.clip(
            -0.24738095238096944*x_lut
            +3.063214285714324*x_lut**2
            -4.527976190476227*x_lut**3
            +1.9821428571428705*x_lut**4,
            0, 1
        )
        
        # Apply LUT using interpolation
        self.env_maps["water_cutoff"] = np.interp(
            self.env_maps["precipitation"], x_lut, y_lut
        )