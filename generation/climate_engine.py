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
        
        small_w = math.ceil(cx / step)
        small_h = math.ceil(cy / step)
        
        small_map = np.zeros((small_w, small_h), dtype=np.float32)
        
        start_world_x = chunk_x * cx
        start_world_y = chunk_y * cy
        
        for i in range(small_w):
            for j in range(small_h):
                
 
                pixel_x = (i * step) + (step // 2)
                pixel_y = (j * step) + (step // 2)
                
               
                pixel_x = min(pixel_x, cx - 1)
                pixel_y = min(pixel_y, cy - 1)

                trace_x = start_world_x + pixel_x
                trace_y = start_world_y + pixel_y
                
                current_moisture = 0.0
                
                for s in range(settings.MAX_STEPS):
                  
                    alt = self.terrain.get_noise_at(trace_x, trace_y)
                    
                    if alt < settings.SEA_LEVEL:
                        current_moisture += settings.MOISTURE_PICKUP
                        if current_moisture >= 1.0:
                            current_moisture = 1.0
                            break
                    elif alt > 0.5: 

                        height_excess = alt - 0.5
                        moisture_loss = height_excess * settings.MOUNTAIN_COST 
                        
                        current_moisture -= moisture_loss
                    else:
                        current_moisture -= settings.DECAY_ON_LAND
                    
                    wx, wy = self.wind.get_wind_at(trace_x, trace_y)
                    mag = math.sqrt(wx*wx + wy*wy)
                    if mag == 0: mag = 1
                    
                    trace_x -= (wx / mag) * settings.STEP_SIZE
                    trace_y -= (wy / mag) * settings.STEP_SIZE
                
              
                small_map[i, j] = max(0.0, min(1.0, current_moisture))
                
        if step == 1:
            return small_map
            
   
        zoom_x = cx / small_w
        zoom_y = cy / small_h
        
   
        precip_map = scipy.ndimage.zoom(small_map, (zoom_x, zoom_y), order=1)
        
        return np.clip(precip_map, 0.0, 1.0)