# generation/climate_engine.py
import numpy as np
import math
import scipy.ndimage # <--- NEW IMPORT
import settings

class ClimateEngine:
    def __init__(self, terrain_engine, wind_engine):
        self.terrain = terrain_engine
        self.wind = wind_engine
        
    def get_precipitation_map(self, chunk_x, chunk_y):
        cx = int(settings.CHUNK_SIZE.x)
        cy = int(settings.CHUNK_SIZE.y)
        step = settings.CLIMATE_STEP
        
        # 1. Create a SMALLER array (e.g., 8x8 instead of 32x32)
        # We use ceil/int division to determine the small size
        small_w = math.ceil(cx / step)
        small_h = math.ceil(cy / step)
        
        # Temporary low-res map
        small_map = np.zeros((small_w, small_h), dtype=np.float32)
        
        start_world_x = chunk_x * cx
        start_world_y = chunk_y * cy
        
        # 2. Loop through the SMALL grid
        for i in range(small_w):
            for j in range(small_h):
                
                # Map small grid index (0, 1, 2) back to world pixels (0, 4, 8)
                # We add 'step // 2' to sample the CENTER of the block, not the corner (better accuracy)
                pixel_x = (i * step) + (step // 2)
                pixel_y = (j * step) + (step // 2)
                
                # Ensure we don't go out of bounds (edge case)
                pixel_x = min(pixel_x, cx - 1)
                pixel_y = min(pixel_y, cy - 1)

                trace_x = start_world_x + pixel_x
                trace_y = start_world_y + pixel_y
                
                current_moisture = 0.0
                
                # --- TRACE LOGIC (Same as before) ---
                for s in range(settings.MAX_STEPS):
                    # We use get_noise_at for single point
                    alt = self.terrain.get_noise_at(trace_x, trace_y)
                    
                    if alt < settings.SEA_LEVEL:
                        current_moisture += settings.MOISTURE_PICKUP
                        if current_moisture >= 1.0:
                            current_moisture = 1.0
                            break
                    elif alt > 0.6: 
                        current_moisture -= settings.MOUNTAIN_COST
                    else:
                        current_moisture -= settings.DECAY_ON_LAND
                    
                    wx, wy = self.wind.get_wind_at(trace_x, trace_y)
                    mag = math.sqrt(wx*wx + wy*wy)
                    if mag == 0: mag = 1
                    
                    trace_x -= (wx / mag) * settings.STEP_SIZE
                    trace_y -= (wy / mag) * settings.STEP_SIZE
                
                # Save to the small map
                small_map[i, j] = max(0.0, min(1.0, current_moisture))
                
        # 3. UPSCALING (The Optimization Magic)
        # If step is 1, just return the map (no optimization)
        if step == 1:
            return small_map
            
        # Use Scipy to smooth-scale the 8x8 map back to 32x32
        # zoom factors: (target_width / current_width, target_height / current_height)
        zoom_x = cx / small_w
        zoom_y = cy / small_h
        
        # order=1 is Bilinear (smooth), order=0 is Nearest (blocky)
        # We use order=1 for nice soft gradients
        precip_map = scipy.ndimage.zoom(small_map, (zoom_x, zoom_y), order=1)
        
        # Clipping again just in case interpolation went slightly out of bounds
        return np.clip(precip_map, 0.0, 1.0)