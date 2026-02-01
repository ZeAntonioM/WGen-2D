import numpy as np
import math
import settings

class ClimateEngine:
    def __init__(self, terrain_engine, wind_engine):
        self.terrain = terrain_engine
        self.wind = wind_engine
        
    def get_precipitation_map(self, chunk_x, chunk_y):
        """
        Generates a 32x32 (or CHUNK_SIZE) map of moisture values (0.0 to 1.0).
        """
        cx = int(settings.CHUNK_SIZE.x)
        cy = int(settings.CHUNK_SIZE.y)
        precip_map = np.zeros((cx, cy), dtype=np.float32)
        
        # Calculate world coordinates for the top-left of this chunk
        start_world_x = chunk_x * cx
        start_world_y = chunk_y * cy
        
        # --- THE TRACE PARAMETERS ---
        # Tuning these changes the climate significantly!
        MAX_STEPS = 10         # How far back do we check? (10 steps)
        STEP_SIZE = 40.0       # How big is one step? (40 pixels)
        MOISTURE_PICKUP = 0.15 # How much water do we gain per step over ocean?
        DECAY_ON_LAND = 0.02   # How much water do we lose simply traveling over land?
        MOUNTAIN_COST = 0.3    # How much water do mountains block?
        
        # Loop through every pixel in the chunk
        # (Optimization Note: In the future, we can do this for every 4th pixel and interpolate)
        for x in range(cx):
            for y in range(cy):
                
                current_moisture = 0.0
                
                # Start tracing backwards from this pixel
                trace_x = start_world_x + x
                trace_y = start_world_y + y
                
                for step in range(MAX_STEPS):
                    # 1. Check Altitude at current trace location
                    # Note: We use get_noise_at because get_noise_height_map generates a whole array
                    # We need a single value.
                    alt = self.terrain.get_noise_at(trace_x, trace_y)
                    
                    # 2. Logic: Where are we?
                    if alt < settings.SEA_LEVEL:
                        # We are over ocean! Pick up moisture.
                        current_moisture += MOISTURE_PICKUP
                        if current_moisture >= 1.0:
                            current_moisture = 1.0
                            break # Max moisture reached, stop tracing
                    
                    elif alt > 0.6: 
                        # High mountain! Rain shadow effect.
                        # If we hit a mountain *upwind*, it blocked the rain getting to us.
                        current_moisture -= MOUNTAIN_COST
                    
                    else:
                        # Normal land, slight decay
                        current_moisture -= DECAY_ON_LAND
                    
                    # 3. Move Backwards
                    # Get wind vector (range -1 to 1)
                    wx, wy = self.wind.get_wind_at(trace_x, trace_y)
                    
                    # Move against the wind (subtract vector)
                    # Simple normalization to keep step size consistent
                    mag = math.sqrt(wx*wx + wy*wy)
                    if mag == 0: mag = 1
                    
                    trace_x -= (wx / mag) * STEP_SIZE
                    trace_y -= (wy / mag) * STEP_SIZE
                    
                # Store final result for this pixel
                precip_map[x, y] = max(0.0, min(1.0, current_moisture))
                
        return precip_map