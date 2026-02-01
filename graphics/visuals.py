import pygame
import math
import settings 
import numpy as np
from generation.biome_placement import biome_vectors_to_rgb

def draw_infinite_grid(surface, camera_pos, chunk_size):
    """ Draws grid lines aligned with chunk boundaries. """
    screen_w, screen_h = surface.get_size()
    view_left = int(camera_pos.x - screen_w // 2)
    view_top = int(camera_pos.y - screen_h // 2)
    
    step_x = int(chunk_size.x)
    step_y = int(chunk_size.y)
    
    # Snap to the nearest grid line
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
            
            # Use the engine passed in the arguments
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
    # 1. Unloaded State
    if not is_loaded:
        surface.fill((60, 40, 40)) # Dark Red placeholder
        return

    # 2. Get Data
    alt = env_maps["altitude"]
    temp = env_maps["temperature"]
    precip = env_maps["precipitation"]

    # 3. Handle Modes
    
    # MODE: ALTITUDE (Grayscale)
    if mode == "altitude":
        c = (alt * 255).astype(np.uint8)
        rgb = np.dstack((c, c, c))
        pygame.surfarray.blit_array(surface, rgb)
        return

    # MODE: TEMPERATURE (Red/Blue Heatmap)
    if mode == "temperature":
        c = (temp * 255).astype(np.uint8)
        # Red = Hot, Blue = Cold
        rgb = np.dstack((c, np.zeros_like(c), 255 - c))
        pygame.surfarray.blit_array(surface, rgb)
        return

    # MODE: PRECIPITATION (Blue Scale)
    if mode == "precipitation":
        c = (precip * 255).astype(np.uint8)
        # Cyan/Blue color
        rgb = np.dstack((np.zeros_like(c), c, c))
        pygame.surfarray.blit_array(surface, rgb)
        return

    # MODE: BIOMES (Standard View)
    if mode == "biomes":
        WATER_LEVEL = settings.SEA_LEVEL
        WATER_COLOR = [0.0, 0.1, 0.3]
        
        water_mask = alt <= WATER_LEVEL
        
        # Get base biome colors
        biome_colors = biome_vectors_to_rgb(env_maps["biomes"])
        
        # Apply Water Color
        # We divide by WATER_LEVEL to normalize brightness relative to depth if desired,
        # or just set it flat.
        biome_colors[water_mask] = np.array(WATER_COLOR) / WATER_LEVEL
        
        # Apply Altitude Shadows (Brightness)
        colors = biome_colors * alt[:, :, np.newaxis]
        
        # Blit to Pygame Surface
        pygame_colors = np.clip((colors * 255).astype(np.uint8), 0, 255)
        pygame.surfarray.blit_array(surface, pygame_colors)
        return