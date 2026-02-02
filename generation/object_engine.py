# generation/object_engine.py
import numpy as np
import settings
from generation.biome_placement import Biome

class WorldObject:
    NONE = 0
    TREE = 1
    CACTUS = 2
    PALM = 3
    ROCK = 4
    SNOW_TREE = 5
    FLOWER = 6
    DEAD_BUSH = 7
    MUSHROOM = 8
    BERRY_BUSH = 9

class ObjectEngine:
    def __init__(self, global_seed):
        self.global_seed = global_seed
        
    def generate_object_map(self, chunk_x, chunk_y, biome_data):
        """
        Returns a 32x32 array of integers representing objects.
        """
        cx = int(settings.CHUNK_SIZE.x)
        cy = int(settings.CHUNK_SIZE.y)
        
        ix = int(chunk_x)
        iy = int(chunk_y)
        
        chunk_seed = (self.global_seed ^ (ix * 73856093)) ^ (iy * 19349663)
        rng = np.random.default_rng(abs(chunk_seed))
        
        if biome_data.ndim == 3:
            biome_map = np.argmax(biome_data, axis=2)
        else:
            biome_map = biome_data


        chance_map = rng.random((cx, cy), dtype=np.float32)
        object_map = np.zeros((cx, cy), dtype=np.uint8)
        
        # --- RULES---
        
        # Rule 1: Temperate Forests 
        mask_forest = (biome_map == Biome.TEMPERATE_FOREST.value)
        object_map[mask_forest & (chance_map < 0.10)] = WorldObject.TREE
        
        # Rule 2: Rainforests 
        mask_rainforest = (biome_map == Biome.TEMPERATE_RAINFOREST.value) | \
                          (biome_map == Biome.TROPICAL_RAINFOREST.value)
        object_map[mask_rainforest & (chance_map < 0.20)] = WorldObject.TREE
        
        # Rule 3: Deserts 
        mask_desert = (biome_map == Biome.SUBTROPICAL_DESERT.value)
        object_map[mask_desert & (chance_map < 0.02)] = WorldObject.CACTUS
        
        # Rule 4: Tropical 
        mask_tropical = (biome_map == Biome.TROPICAL_SEASONAL_FOREST.value)
        object_map[mask_tropical & (chance_map < 0.05)] = WorldObject.PALM

        # Rule 5: Taiga 
        mask_taiga = (biome_map == Biome.TAIGA.value)
        object_map[mask_taiga & (chance_map < 0.10)] = WorldObject.SNOW_TREE

        # Rule 6: Rocks in High Mountains
        mask_tundra = (biome_map == Biome.TUNDRA.value)
        
        object_map[mask_tundra & (chance_map < 0.04)] = WorldObject.ROCK



        # Rule 7: Wildflowers in Temperate Grassland
        mask_grassland = (biome_map == Biome.TEMPERATE_GRASSLAND.value)
        object_map[mask_grassland & (chance_map < 0.01)] = WorldObject.FLOWER

        # Rule 8: Dead Bushes in Desert 
        mask_desert = (biome_map == Biome.SUBTROPICAL_DESERT.value)
        object_map[mask_desert & (chance_map > 0.98)] = WorldObject.DEAD_BUSH
        mask_desert = (biome_map == Biome.SUBTROPICAL_DESERT.value)
        object_map[mask_desert & (chance_map > 0.99)] = WorldObject.ROCK


        # Rule 9: Mushrooms in Rainforests 
        mask_jungle = (biome_map == Biome.TROPICAL_RAINFOREST.value) | \
                      (biome_map == Biome.TEMPERATE_RAINFOREST.value)

        object_map[mask_jungle & (chance_map > 0.99)] = WorldObject.MUSHROOM

        # Rule 10: Berry Bushes in Taiga 
        mask_taiga = (biome_map == Biome.TAIGA.value)
        object_map[mask_taiga & (chance_map > 0.90)] = WorldObject.BERRY_BUSH
        
        return object_map