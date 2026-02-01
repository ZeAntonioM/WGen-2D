import numpy as np
from noise import snoise2 # Simplex noise

class WindEngine:
    def __init__(self, seed, scale=2000.0):
        self.seed_x = seed + 100 # Offset to ensure X and Y noise aren't identical
        self.seed_y = seed + 200
        self.scale = scale # High scale means the wind changes slowly over long distances

    def get_wind_at(self, x, y):
        # 1. Sample two noise maps for the X and Y components of the wind vector
        # snoise2 returns values between -1.0 and 1.0
        nx = snoise2(x / self.scale, y / self.scale, octaves=2, base=self.seed_x)
        ny = snoise2(x / self.scale, y / self.scale, octaves=2, base=self.seed_y)
        
        # 2. Convert to a direction (radians) and magnitude
        # We can treat nx and ny as a force vector
        angle = np.arctan2(ny, nx) 
        magnitude = np.sqrt(nx**2 + ny**2) # Wind speed
        
        return angle, magnitude