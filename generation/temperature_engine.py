import numpy as np
import settings

class TemperatureEngine():
    
    def __init__(self, smooth_altitude_noise_engine, temperature_noise_engine):
        self.alt = smooth_altitude_noise_engine
        self.temperature = temperature_noise_engine
        
    def get_temperature_at(self, x: int, y: int) -> float:
        """
        Returns the temperature (between 0.0 and 1.0) for
        a single global coordinate (x, y)
        """
        return np.clip(
            (1+settings.COLD_MOUNTAINS)*self.temperature.get_normalized_noise_at(x, y) \
            - settings.COLD_MOUNTAINS*self.alt.get_normalized_noise_at(x, y),
            0, 1
        )

    def get_temperature_map(self, chunk_x: int, chunk_y: int) -> np.array:
        """
        Returns the temperature map of this chunk as a numpy array
        (values between 0.0 and 1.0).
        """
        return np.clip(
            (1+settings.COLD_MOUNTAINS)*self.temperature.get_noise_height_map(chunk_x, chunk_y) \
            - settings.COLD_MOUNTAINS*self.alt.get_noise_height_map(chunk_x, chunk_y),
            0, 1
        )
