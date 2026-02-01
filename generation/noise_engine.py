#!/usr/bin/python

import numpy as np
from pyfastnoiselite.pyfastnoiselite import FastNoiseLite, NoiseType, FractalType
import settings  # Import settings to get CHUNK_SIZE

class NoiseEngine:
    """
    There should only be one instance of this class.
    This class is responsible for generating noise values for terrain generation.
    """
    
    # Updated __init__ to accept fractal_octaves
    def __init__(self, seed, frequency=0.01, fractal_octaves=5):
        # Use the global setting instead of hardcoded 32
        self.chunk_size = int(settings.CHUNK_SIZE.x)
        
        # initialize FastNoiseLite with seed
        self.noise = FastNoiseLite(seed)
        
        # Following the original Paper: Simplex noise and FBm fractal.
        self.noise.noise_type = NoiseType.NoiseType_OpenSimplex2
        self.noise.fractal_type = FractalType.FractalType_FBm
        
        # Use the passed argument instead of the hardcoded value
        self.noise.fractal_octaves = fractal_octaves
        
        self.noise.frequency = frequency
        
    """
    Generate a height map for a given chunk using FastNoiseLite.
    
    @param chunk_x: The x coordinate of the chunk (tile index).
    @param chunk_y: The y coordinate of the chunk (tile index).
    @return: A 2D numpy array representing the height map for the chunk.
    """    
    def get_noise_height_map(self, chunk_x, chunk_y):
        
        height_map = np.zeros((self.chunk_size, self.chunk_size), dtype=np.float32)
        
        # Calculate world coordinates offset
        start_x = float(chunk_x * self.chunk_size)
        start_y = float(chunk_y * self.chunk_size)
        
        for y in range(self.chunk_size):
            world_y = start_y + y
            
            for x in range(self.chunk_size):
                world_x = start_x + x

                noise_value = self.noise.get_noise(world_x, world_y)
                
                # Normalize from -1..1 to 0..1
                height_map[x, y] = (noise_value + 1) / 2.0

        return height_map