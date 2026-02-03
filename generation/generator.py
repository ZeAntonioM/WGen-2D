import pygame

import settings
from generation.noise_engine import NoiseEngine
from generation.terrain_engine import TerrainEngine
from generation.climate_engine import ClimateEngine
from generation.wind_engine import WindEngine
from generation.water_engine import WaterEngine
from generation.object_engine import ObjectEngine
from generation.river_engine import RiverEngine


class Generator():
    
    def __init__(self, seed):
        self.seed = seed
        
        self._setup_engines()

    def _setup_engines(self):
        altitude_seed = self.seed + 10
        temperature_seed = self.seed + 11
        wind_seed = self.seed + 12
        object_seed = self.seed + 13
        river_seed = self.seed + 14
        
        altitude_noise_engine = NoiseEngine(
            seed=altitude_seed,
            frequency=settings.ALTITUDE_NOISE_FREQUENCY,
            fractal_octaves=settings.ALTITUDE_NOISE_OCTAVES
        )
        self.temperature_noise_engine = NoiseEngine(
            seed=temperature_seed,
            frequency=settings.TEMPERATURE_NOISE_FREQUENCY,
            fractal_octaves=settings.TEMPERATURE_NOISE_OCTAVES
        )
        self.wind_engine = WindEngine(seed=wind_seed, scale=settings.WIND_SCALE)
        river_noise_engine = NoiseEngine(
            seed=river_seed,
            frequency=settings.RIVER_NOISE_FREQUENCY,
            fractal_octaves=settings.RIVER_NOISE_OCTAVES
        )

        self.river_engine = RiverEngine(river_noise_engine)
        self.terrain_engine = TerrainEngine(altitude_noise_engine, self.river_engine)
        self.water_engine = WaterEngine(self.temperature_noise_engine)
        self.climate_engine = ClimateEngine(self.terrain_engine, self.water_engine, self.wind_engine)
        self.object_engine = ObjectEngine(seed=object_seed)
