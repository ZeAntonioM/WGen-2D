import numpy as np
import settings
from world.utils import apply_function_to_map

class WaterEngine():
    
    def __init__(self, temperature_noise_engine):
        self.temperature = temperature_noise_engine
        
    def get_water_level_at(self, x: int, y: int) -> float:
        """
        Returns the water level (between 0.0 and 1.0) for
        a single global coordinate (x, y)
        """
        return settings.WATER_LEVEL_RESHAPING_FUNCTION(1.0-self.temperature.get_normalized_noise_at(x, y))

    def get_water_level_map(self, chunk_x: int, chunk_y: int) -> np.array:
        """
        Returns the water level map of this chunk as a numpy array
        (values between 0.0 and 1.0).
        """
        return apply_function_to_map(
            settings.WATER_LEVEL_RESHAPING_FUNCTION,
            (1.0-self.temperature.get_noise_height_map(chunk_x, chunk_y))
        )
