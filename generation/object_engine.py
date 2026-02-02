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

class ObjectEngine:
    def __init__(self, global_seed):
        self.global_seed = global_seed
        
    def generate_object_map(self, chunk_x, chunk_y, biome_data):
        """
        Returns a 32x32 array of integers representing objects.
        """
        cx = int(settings.CHUNK_SIZE.x)
        cy = int(settings.CHUNK_SIZE.y)
        
        # --- FIX 1: FORCE INTEGERS FOR SEED ---
        ix = int(chunk_x)
        iy = int(chunk_y)
        
        chunk_seed = (self.global_seed ^ (ix * 73856093)) ^ (iy * 19349663)
        rng = np.random.default_rng(abs(chunk_seed))
        
        # --- FIX 2: HANDLE 3D BIOME MAPS ---
        # If biome_data is (32, 32, 9), it contains weights for blending.
        # We need to convert it to (32, 32) IDs to check "What biome is this?"
        if biome_data.ndim == 3:
            # np.argmax returns the index of the highest value along the last axis
            # This gives us the dominant biome ID for that pixel
            biome_map = np.argmax(biome_data, axis=2)
        else:
            # It's already 2D
            biome_map = biome_data

        # 3. Generate Chance Map
        chance_map = rng.random((cx, cy), dtype=np.float32)
        
        # 4. Create Object Map
        object_map = np.zeros((cx, cy), dtype=np.uint8)
        
        # --- RULES (Now using the collapsed biome_map) ---
        
        # Rule 1: Temperate Forests (20%)
        mask_forest = (biome_map == Biome.TEMPERATE_FOREST.value)
        object_map[mask_forest & (chance_map < 0.10)] = WorldObject.TREE
        
        # Rule 2: Rainforests (40%)
        mask_rainforest = (biome_map == Biome.TEMPERATE_RAINFOREST.value) | \
                          (biome_map == Biome.TROPICAL_RAINFOREST.value)
        object_map[mask_rainforest & (chance_map < 0.20)] = WorldObject.TREE
        
        # Rule 3: Deserts (2%)
        mask_desert = (biome_map == Biome.SUBTROPICAL_DESERT.value)
        object_map[mask_desert & (chance_map < 0.02)] = WorldObject.CACTUS
        
        # Rule 4: Tropical (10%)
        mask_tropical = (biome_map == Biome.TROPICAL_SEASONAL_FOREST.value)
        object_map[mask_tropical & (chance_map < 0.05)] = WorldObject.PALM

        # Rule 5: Taiga (15%)
        mask_taiga = (biome_map == Biome.TAIGA.value)
        object_map[mask_taiga & (chance_map < 0.10)] = WorldObject.SNOW_TREE
        # Rule 6: Rocks in High Mountains (Tundra)
        # Since Tundra is your "Mountain Top" biome, this works perfectly.
        mask_tundra = (biome_map == Biome.TUNDRA.value)
        
        # Give them a 5-10% chance so they are scattered but noticeable
        object_map[mask_tundra & (chance_map < 0.04)] = WorldObject.ROCK

        # Optional: Rocks in the Desert (Rocky Desert)
        # Use a different random range (> 0.98) so you don't overwrite Cacti (< 0.02)
        mask_desert = (biome_map == Biome.SUBTROPICAL_DESERT.value)
        object_map[mask_desert & (chance_map > 0.99)] = WorldObject.ROCK
        
        return object_map