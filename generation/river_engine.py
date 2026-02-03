import numpy as np
import settings
from world.utils import apply_function_to_map

class RiverEngine():
    
    def __init__(self, river_noise_engine):
        self.riv = river_noise_engine
        
    def get_river_at(self, x: int, y: int) -> float:
        """
        Returns the river (between 0.0 and 1.0) for
        a single global coordinate (x, y)
        """
        return settings.RIVER_RESHAPING_FUNCTION(self.riv.get_normalized_noise_at(x, y))

    def get_river_map(self, chunk_x: int, chunk_y: int) -> np.array:
        """
        Returns the river map of this chunk as a numpy array
        (values between 0.0 and 1.0).
        """
        return apply_function_to_map(
            settings.RIVER_RESHAPING_FUNCTION,
            self.riv.get_noise_height_map(chunk_x, chunk_y)
        )
