import numpy as np
import settings
from world.utils import apply_function_to_map

class RiverEngine():
    
    def __init__(self, altitude_noise_engine, water_engine, river_noise_engine):
        self.alt = altitude_noise_engine
        self.water_level = water_engine
        self.riv = river_noise_engine
        
    def get_river_at(self, x: int, y: int) -> float:
        """
        Returns the river (between 0.0 and 1.0) for
        a single global coordinate (x, y)
        """
        height_diff = self.alt.get_normalized_noise_at(x, y) - self.water_level.get_water_level_at(x, y)
        a = settings.AVOID_MOUNTAINS
        return settings.RIVER_RESHAPING_FUNCTION(
            np.clip(a*height_diff + (1-a)*self.riv.get_normalized_noise_at(x, y), 0, 1)
        )

    def get_river_map(self, chunk_x: int, chunk_y: int) -> np.array:
        """
        Returns the river map of this chunk as a numpy array
        (values between 0.0 and 1.0).
        """
        height_diff = self.alt.get_noise_height_map(chunk_x, chunk_y) - self.water_level.get_water_level_map(chunk_x, chunk_y)
        a = settings.AVOID_MOUNTAINS
        return apply_function_to_map(
            settings.RIVER_RESHAPING_FUNCTION,
            np.clip(a*height_diff + (1-a)*self.riv.get_noise_height_map(chunk_x, chunk_y), 0, 1)
        )
