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
        
        height_map = np.zeros((int(settings.CHUNK_SIZE.x), int(settings.CHUNK_SIZE.y)), dtype=np.float32)
        
        # Calculate world coordinates offset
        start_x = float(chunk_x * settings.CHUNK_SIZE.x)
        start_y = float(chunk_y * settings.CHUNK_SIZE.y)
        
        for y in range(int(settings.CHUNK_SIZE.y)):
            world_y = start_y + y
            
            for x in range(int(settings.CHUNK_SIZE.x)):
                world_x = start_x + x

                noise_value = self.noise.get_noise(world_x, world_y)
                
                # Normalize from -1..1 to 0..1
                height_map[x, y] = (noise_value + 1) / 2.0

        return height_map
    
    def get_raw_noise_at(self, x, y):
        """
        Returns a single noise value at world coordinates x, y.
        Range: -1.0 to 1.0 (Raw noise)
        """
        return self.noise.get_noise(float(x), float(y))
    def get_normalized_noise_at(self, x, y):
        """
        Returns a single noise value at world coordinates x, y.
        Range: 0.0 to 1.0 (Normalized noise)
        """
        return (self.noise.get_noise(float(x), float(y))+1)/2
