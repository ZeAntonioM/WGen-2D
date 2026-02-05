import numpy as np
import settings
from world.utils import apply_function_to_map

class TerrainEngine():
    
    def __init__(self, altitude_noise_engine, river_engine):
        self.alt = altitude_noise_engine
        self.river = river_engine
        
    def get_terrain_at(self, x: int, y: int) -> float:
        """
        Returns the terrain height (between 0.0 and 1.0) for
        a single global coordinate (x, y)
        """
        terr = settings.ALTITUDE_RESHAPING_FUNCTION(self.alt.get_normalized_noise_at(x, y))
        return terr * (1-self.river.get_river_at(x, y))

    def get_terrain_map(self, chunk_x: int, chunk_y: int) -> np.array:
        """
        Returns the terrain height map of this chunk as a numpy array
        (values between 0.0 and 1.0).
        """
        terr = apply_function_to_map(
            settings.ALTITUDE_RESHAPING_FUNCTION,
            self.alt.get_noise_height_map(chunk_x, chunk_y)
        )
        return terr * (1-self.river.get_river_map(chunk_x, chunk_y))
