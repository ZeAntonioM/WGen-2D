import numpy as np
import settings
from world.utils import apply_function_to_map

class TerrainEngine():
    
    def __init__(self, altitude_noise_engine):
        self.alt = altitude_noise_engine
        
    def get_terrain_at(self, x: int, y: int) -> float:
        """
        Returns the water level (between 0.0 and 1.0) for
        a single global coordinate (x, y)
        """
        return settings.ALTITUDE_RESHAPING_FUNCTION(self.alt.get_normalized_noise_at(x, y))

    def get_terrain_map(self, chunk_x: int, chunk_y: int) -> np.array:
        """
        Returns the water level map of this chunk as a numpy array
        (values between 0.0 and 1.0).
        """
        return apply_function_to_map(
            settings.ALTITUDE_RESHAPING_FUNCTION,
            self.alt.get_noise_height_map(chunk_x, chunk_y)
        )
