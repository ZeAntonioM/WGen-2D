import settings
from generation.noise_engine import NoiseEngine
from generation.terrain_engine import TerrainEngine
from generation.climate_engine import ClimateEngine
from generation.wind_engine import WindEngine
from generation.water_engine import WaterEngine

ALTITUDE_NOISE_ENGINE = NoiseEngine(
    seed=settings.ALTITUDE_NOISE_SEED,
    frequency=settings.ALTITUDE_NOISE_FREQUENCY,
    fractal_octaves=settings.ALTITUDE_NOISE_OCTAVES
)
TEMPERATURE_NOISE_ENGINE = NoiseEngine(
    seed=settings.TEMPERATURE_NOISE_SEED,
    frequency=settings.TEMPERATURE_NOISE_FREQUENCY,
    fractal_octaves=settings.TEMPERATURE_NOISE_OCTAVES
)
WIND_ENGINE = WindEngine(seed=settings.WIND_SEED, scale=settings.WIND_SCALE)
TERRAIN_ENGINE = TerrainEngine(ALTITUDE_NOISE_ENGINE)
WATER_ENGINE = WaterEngine(TEMPERATURE_NOISE_ENGINE)
CLIMATE_ENGINE = ClimateEngine(TERRAIN_ENGINE, WATER_ENGINE, WIND_ENGINE)
