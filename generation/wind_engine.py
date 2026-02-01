# generation/wind_engine.py
import numpy as np
import settings
from generation.noise_engine import NoiseEngine

class WindEngine:
    def __init__(self, seed, scale=2000.0):
  
        frequency = 1.0 / scale
  
        self.noise_x = NoiseEngine(
            seed=seed + 100, 
            frequency=frequency,
            fractal_octaves=2 
        )
        
        self.noise_y = NoiseEngine(
            seed=seed + 200, 
            frequency=frequency,
            fractal_octaves=2
        )

    def get_wind_at(self, x, y):

        nx = self.noise_x.get_noise_at(x, y)
        ny = self.noise_y.get_noise_at(x, y)
        
        angle = np.arctan2(ny, nx) 
        magnitude = np.sqrt(nx**2 + ny**2)
        
        return angle, magnitude 