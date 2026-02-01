#!/usr/bin/python

import numpy as np
from pyfastnoiselite.pyfastnoiselite import FastNoiseLite, NoiseType, FractalType

from src.simulation_constants import *


class NoiseEngine:

    def __init__(self, seed, frequency=0.01, fractal_octaves=5):
        """
        This class is resposible for generating noise values for terrain generation.
        FastNoiseLite is used for noise generation, and the main parameters are set at initialization. 
        For multiple different height maps, instance this engine multiple times.
        
        @param seed: The seed for the noise generation. Should be randomized for different worlds, or given by the user for consistent worlds.
        @param frequency: The frequency of the noise.
        """
        
        # initialize FastNoiseLite with seed
        self.noise = FastNoiseLite(seed)
        
        # Following the original Paper, we should set the Noise type to simplex, and Fractal type to FBm.
        self.noise.noise_type = NoiseType.NoiseType_OpenSimplex2
        self.noise.fractal_type = FractalType.FractalType_FBm
        
        # The number of octaves determines how much detail is added to the noise.
        self.noise.fractal_octaves = fractal_octaves
        
        # Depending on the desired terrain, we should set the frequency appropriately.
        # A lower frequency created larger biomes, while a higher frequency creates smaller biomes.
        self.noise.frequency = frequency
        
        
    
    def get_noise_height_map(self, chunk_x, chunk_y) -> np.array:
        """
        Generate a height map for a given chunk using FastNoiseLite.
        
        @param chunk_x: The x coordinate of the chunk. Must be the "world"/tile coordinate, not the local chunk coordinate.
        @param chunk_y: The y coordinate of the chunk. Must be the "world"/tile coordinate, not the local chunk coordinate.
        @return: A 2D numpy array representing the height map for the chunk.
        """
        
        # We create a height map of size chunk_size x chunk_size, as each chunk is of that size. Built it in a scalable way so that we can change chunk size later if needed.
        height_map = np.zeros((int(CHUNK_SIZE.x), int(CHUNK_SIZE.y)), dtype=np.float32)
        start_x = float(chunk_x * CHUNK_SIZE.x)
        start_y = float(chunk_y * CHUNK_SIZE.y)
        
        for y in range(int(CHUNK_SIZE.y)):
            world_y = start_y + y
            
            for x in range(int(CHUNK_SIZE.x)):
                world_x = start_x + x

                noise_value = self.noise.get_noise(world_x, world_y)
                
                # Simple normalization from -1 to 1 range to 0 to 1 range. When used at generation time, this will be scaled to the desired height.
                height_map[x, y] = (noise_value + 1) / 2.0

        return height_map

