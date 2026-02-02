import pygame
import math
import settings 
import numpy as np
from generation.biome_placement import biome_vectors_to_rgb
from generation.object_engine import WorldObject

def draw_infinite_grid(surface, camera_pos, chunk_size):
    """ Draws grid lines aligned with chunk boundaries. """
    screen_w, screen_h = surface.get_size()
    view_left = int(camera_pos.x - screen_w // 2)
    view_top = int(camera_pos.y - screen_h // 2)
    
    step_x = int(chunk_size.x)
    step_y = int(chunk_size.y)
    
    start_x = view_left - (view_left % step_x)
    start_y = view_top - (view_top % step_y)
    
    # Draw Vertical Lines
    for world_x in range(start_x, view_left + screen_w + step_x, step_x):
        screen_x = world_x - view_left
        pygame.draw.line(surface, settings.COLOR_GRID, (screen_x, 0), (screen_x, screen_h), 2)
        
    # Draw Horizontal Lines
    for world_y in range(start_y, view_top + screen_h + step_y, step_y):
        screen_y = world_y - view_top
        pygame.draw.line(surface, settings.COLOR_GRID, (0, screen_y), (screen_w, screen_y), 2)


def draw_wind_arrows(surface, camera_pos, wind_engine, grid_spacing=64):
    """ 
    Draws wind vectors. 
    Notice we pass 'wind_engine' as an argument so this function 
    can query the data it needs.
    """
    screen_w, screen_h = surface.get_size()
    view_left = int(camera_pos.x - screen_w // 2)
    view_top = int(camera_pos.y - screen_h // 2)

    start_x = view_left - (view_left % grid_spacing)
    start_y = view_top - (view_top % grid_spacing)

    for x in range(start_x, view_left + screen_w + grid_spacing, grid_spacing):
        for y in range(start_y, view_top + screen_h + grid_spacing, grid_spacing):
            
            vx, vy = wind_engine.get_wind_at(x, y)
            
            screen_x = x - view_left
            screen_y = y - view_top

            arrow_len = 25
            mag = math.sqrt(vx**2 + vy**2)
            if mag == 0: continue
            
            end_x = screen_x + (vx / mag) * arrow_len
            end_y = screen_y + (vy / mag) * arrow_len
            
            pygame.draw.line(surface, settings.COLOR_WIND, (screen_x, screen_y), (end_x, end_y), 2)
            pygame.draw.circle(surface, settings.COLOR_WIND, (int(screen_x), int(screen_y)), 3)


def update_chunk_surface(surface, env_maps, is_loaded, mode="biomes"):
    """
    Paint the pixels of a chunk surface based on its data.
    """
 
    if not is_loaded:
        surface.fill((60, 40, 40)) 
        return


    alt = env_maps["altitude"]
    temp = env_maps["temperature"]
    precip = env_maps["precipitation"]

    if "water_cutoff" in env_maps and env_maps["water_cutoff"] is not None:
        water_cutoff = env_maps["water_cutoff"]
    else:
        water_cutoff = np.full_like(alt, settings.SEA_LEVEL)

    # Debug modes
    if mode == "altitude":
        c = (alt * 255).astype(np.uint8)
        rgb = np.dstack((c, c, c))
        pygame.surfarray.blit_array(surface, rgb)
        return

  
    if mode == "temperature":
        c = (temp * 255).astype(np.uint8)
        rgb = np.dstack((c, np.zeros_like(c), 255 - c))
        pygame.surfarray.blit_array(surface, rgb)
        return

 
    if mode == "precipitation":
        c = (precip * 255).astype(np.uint8)
        rgb = np.dstack((np.zeros_like(c), c, c))
        pygame.surfarray.blit_array(surface, rgb)
        return

  
    if mode == "biomes":
        WATER_COLOR = np.array([0.0, 0.1, 0.3], dtype=np.float32)
        water_mask = alt <= water_cutoff
        biome_colors = biome_vectors_to_rgb(env_maps["biomes"])
        
        safe_cutoff = np.maximum(water_cutoff, 1e-4)
        biome_colors[water_mask] = (WATER_COLOR / safe_cutoff[water_mask, None])
        
        brightness = alt.copy()
        brightness[~water_mask] = 0.2 + (alt[~water_mask] * 0.8)
        brightness[water_mask] = alt[water_mask]
        colors = biome_colors * brightness[:, :, np.newaxis]
        
        pygame_colors = np.clip((colors * 255).astype(np.uint8), 0, 255)
        pygame.surfarray.blit_array(surface, pygame_colors)
  
    
        if mode == "biomes" and "objects" in env_maps:
            obj_map = env_maps["objects"]
            

            object_locations = np.argwhere(obj_map > 0)
            
            for x, y in object_locations:
                obj_type = obj_map[x, y]
                
                if water_mask[x, y]: 
                    continue

                color = None
                radius = 2
                
                if obj_type == WorldObject.TREE:
                    color = (10, 50, 10)     # Dark Green
                elif obj_type == WorldObject.CACTUS:
                    color = (50, 150, 50)    # Light Green
                    radius = 1
                elif obj_type == WorldObject.PALM:
                    color = (150, 100, 50)   # Brownish
                elif obj_type == WorldObject.SNOW_TREE:
                    color = (200, 220, 220)  # White-ish

                elif obj_type == WorldObject.ROCK:
                    color = (100, 100, 110)  # Slate Grey
                    radius = 2               # Small, distinct dots
                
                if color:
                    # Draw directly onto the chunk surface
                    pygame.draw.circle(surface, color, (x, y), radius)

        return
    