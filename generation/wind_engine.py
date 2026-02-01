# generation/wind_engine.py
import numpy as np
import settings
from generation.noise_engine import NoiseEngine

class WindEngine:
    def __init__(self, seed, scale=2000.0):
        # Frequency is the inverse of scale
        # If scale is 2000, frequency is 0.0005
        frequency = 1.0 / scale
        
        # Create two separate noise engines for X and Y components
        # We offset the seeds so the wind doesn't blow diagonally everywhere
        self.noise_x = NoiseEngine(
            seed=seed + 100, 
            frequency=frequency,
            fractal_octaves=2 # Wind is usually smoother than terrain
        )
        
        self.noise_y = NoiseEngine(
            seed=seed + 200, 
            frequency=frequency,
            fractal_octaves=2
        )

    def get_wind_at(self, x, y):
        # 1. Get the vector components using the unified NoiseEngine
        # Range is -1.0 to 1.0
        nx = self.noise_x.get_noise_at(x, y)
        ny = self.noise_y.get_noise_at(x, y)
        
        # 2. Convert to direction and magnitude
        # This math remains the same
        angle = np.arctan2(ny, nx) 
        magnitude = np.sqrt(nx**2 + ny**2)
        
        return angle, magnitude # Return vector components (easier for tracing) OR angle, magnitude