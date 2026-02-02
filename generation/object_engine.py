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
        cx = int(settings.CHUNK_SIZE.x)
        cy = int(settings.CHUNK_SIZE.y)
        
        ix = int(chunk_x)
        iy = int(chunk_y)
        
        chunk_seed = (self.global_seed ^ (ix * 73856093)) ^ (iy * 19349663)
        rng = np.random.default_rng(abs(chunk_seed))
        
        chance_map = rng.random((cx, cy), dtype=np.float32)
        object_map = np.zeros((cx, cy), dtype=np.uint8)

        def get_weight(biome_enum):
            if biome_data.ndim == 3:
                return biome_data[:, :, biome_enum.value]
            else:
                return (biome_data == biome_enum.value).astype(np.float32)
        
        # Rule 1: Temperate Forests 
        w_forest = get_weight(Biome.TEMPERATE_FOREST)
        object_map[chance_map < (0.10 * w_forest)] = WorldObject.TREE
        
        # Rule 2: Rainforests 
        w_rainforest = get_weight(Biome.TEMPERATE_RAINFOREST) + \
                       get_weight(Biome.TROPICAL_RAINFOREST)
        object_map[chance_map < (0.20 * w_rainforest)] = WorldObject.TREE
        
        # Rule 3: Deserts (Cactus)
        w_desert = get_weight(Biome.SUBTROPICAL_DESERT)
        object_map[chance_map < (0.02 * w_desert)] = WorldObject.CACTUS
        
        # Rule 4: Tropical (Palms)
        w_tropical = get_weight(Biome.TROPICAL_SEASONAL_FOREST)
        object_map[chance_map < (0.05 * w_tropical)] = WorldObject.PALM

        # Rule 5: Taiga (Snow Trees)
        w_taiga = get_weight(Biome.TAIGA)
        object_map[chance_map < (0.10 * w_taiga)] = WorldObject.SNOW_TREE

        # Rule 6: Rocks in High Mountains
        w_tundra = get_weight(Biome.TUNDRA)
        object_map[chance_map < (0.04 * w_tundra)] = WorldObject.ROCK

        # Rule 7: Wildflowers in Temperate Grassland
        w_grassland = get_weight(Biome.TEMPERATE_GRASSLAND)
        object_map[chance_map < (0.005 * w_grassland)] = WorldObject.FLOWER

        # Rule 8: Dead Bushes and Rocks in Desert 
        object_map[chance_map > (1.0 - (0.02 * w_desert))] = WorldObject.DEAD_BUSH
        object_map[chance_map > (1.0 - (0.01 * w_desert))] = WorldObject.ROCK

        # Rule 9: Mushrooms in Rainforests 
        object_map[chance_map > (1.0 - (0.01 * w_rainforest))] = WorldObject.MUSHROOM

        # Rule 10: Berry Bushes in Taiga 
        object_map[chance_map > (1.0 - (0.10 * w_taiga))] = WorldObject.BERRY_BUSH
        
        return object_map