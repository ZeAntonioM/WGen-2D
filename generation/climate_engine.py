import numpy as np
import math
import scipy.ndimage
import settings

class ClimateEngine:
    def __init__(self, terrain_engine, water_engine, wind_engine):
        self.terrain = terrain_engine
        self.water = water_engine
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
                    
                    terrain = self.terrain.get_terrain_at(trace_x, trace_y)
                    water_level = self.water.get_water_level_at(trace_x, trace_y)
                    meters_above_sea = terrain - water_level
                    if meters_above_sea < 0: meters_above_sea = 0

                    # this pickup coefficient is 1 inside water and quickly decreases against 0 with increasing distance to water
                    pickup = max(0.0, min(1.0, 1.0-meters_above_sea))
                    pickup **= 7

                    current_moisture += pickup * settings.MOISTURE_PICKUP / settings.MAX_STEPS
                    if current_moisture >= 1.0:
                        current_moisture = 1.0
                        break
                    if terrain > 0.5: 

                        height_excess = terrain - 0.5
                        moisture_loss = height_excess * settings.MOUNTAIN_COST / settings.MAX_STEPS
                        
                        current_moisture -= moisture_loss
                    else:
                        pass#current_moisture -= settings.DECAY_ON_LAND
                    
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
