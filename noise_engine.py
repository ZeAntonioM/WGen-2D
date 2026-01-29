#!/usr/bin/python

import numpy as np
from pyfastnoiselite.pyfastnoiselite import FastNoiseLite, NoiseType, FractalType


class NoiseEngine:

    """
    There should only be one instance of this class.
    This class is resposible for generating noise values for terrain generation.
    FastnoiseLite is used for noise generation, and the main parameters are set at initialization. 
    
    @param seed: The seed for the noise generation. Should be randomized for different worlds, or given by the user for consistent worlds.
    @param frequency: The frequency of the noise.
    """
    def __init__(self, seed, frequency=0.01):
        self.chunk_size = 32
        
        # initialize FastNoiseLite with seed
        self.noise = FastNoiseLite(seed)
        
        # Following the original Paper, we should set the Noise type to simplex, and Fractal type to FBm.
        self.noise.SetNoiseType(NoiseType.FastNoiseLite_OpenSimplex2)
        self.noise.SetFractalType(FractalType.FastNoiseLite_FractalFBm)
        
        # The number of octaves determines how much detail is added to the noise.
        self.noise.SetFractalOctaves(5)
        
        # Depending on the desired terrain, we should set the frequency appropriately.
        # A lower frequency created larger biomes, while a higher frequency creates smaller biomes.
        self.noise.SetFrequency(frequency)
        
        
    """
    Generate a height map for a given chunk using FastNoiseLite.
    
    @param chunk_x: The x coordinate of the chunk. Must me the "world" coordinate, not the local chunk coordinate.
    @param chunk_y: The y coordinate of the chunk. Must me the "world" coordinate, not the local chunk coordinate.
    @return: A 2D numpy array representing the height map for the chunk.
    """    
    def get_noise_height_map(self, chunk_x, chunk_y):
        
        # We create a height map of size chunk_size x chunk_size, as each chunk is of that size. Built it in a scalable way so that we can change chunk size later if needed.
        height_map = np.zeros((self.chunk_size, self.chunk_size), dtype=np.float32)
        start_x = float(chunk_x * self.chunk_size)
        start_y = float(chunk_y * self.chunk_size)
        
        for y in range(self.chunk_size):
            world_y = start_y + y
            
            for x in range(self.chunk_size):
                world_x = start_x + x

                noise_value = self.noise.GetNoise(world_x, world_y)
                
                # Simple normalization from -1 to 1 range to 0 to 1 range. When used at generation time, this will be scaled to the desired height.
                height_map[y, x] = (noise_value + 1) / 2.0
                
                
