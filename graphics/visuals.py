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


    alt = env_maps["terrain"]
    temp = env_maps["temperature"]
    precip = env_maps["precipitation"]
    water_cutoff = env_maps["water_level"]
    river_map = env_maps["river"]

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

    if mode == "river":
        c = (river_map * 255).astype(np.uint8)
        rgb = np.dstack((np.zeros_like(c), np.zeros_like(c), c))
        pygame.surfarray.blit_array(surface, rgb)
  
    if mode == "biomes":
        WATER_COLOR = np.array([0.0, 0.3, 0.9], dtype=np.float32)
        water_mask = alt <= water_cutoff
        biome_colors = biome_vectors_to_rgb(env_maps["biomes"])
        
        #safe_cutoff = np.maximum(water_cutoff, 1e-4)
        biome_colors[water_mask] = WATER_COLOR#(WATER_COLOR / safe_cutoff[water_mask, None])
        
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
                    radius = 1.5
                elif obj_type == WorldObject.PALM:
                    color = (150, 100, 50)   # Brownish
                elif obj_type == WorldObject.SNOW_TREE:
                    color = (200, 220, 220)  # White-ish

                elif obj_type == WorldObject.ROCK:
                    color = (100, 100, 110)  # Slate Grey
                    radius = 2

                elif obj_type == WorldObject.FLOWER:
                    color = (255, 200, 0)
                    radius = 1               
            
                elif obj_type == WorldObject.DEAD_BUSH:
                    color = (90, 70, 40)    # Dry Brown
                    radius = 1.5

                elif obj_type == WorldObject.MUSHROOM:
                    color = (200, 50, 50)    # Bright Red
                    radius = 2               
                
                elif obj_type == WorldObject.BERRY_BUSH:
                    color = (50, 100, 180)    # Blue-Green bush
                    radius = 1
                
                if color:
                    pygame.draw.circle(surface, color, (x, y), radius)

        return
    

def draw_controls_hud(surface):
    """
    Draws a simple UI overlay showing available controls.
    """
    font = pygame.font.SysFont("monospace", 16, bold=True)
    
    controls = [
        ("1", "Biome Map"),
        ("2", "Altitude Map"),
        ("3", "Temperature Map"),
        ("4", "Precipitation Map"),
        ("5", "River Map"),
        ("W", "Toggle Wind View"),
        ("C", "Toggle Chunk Grid"), 
        ("ESC", "Quit"),
    ]

    screen_w = surface.get_width()
    
 
    x_pos = screen_w - 250 
    y_pos = 10
    line_height = 20
    

    panel_rect = (x_pos - 10, y_pos - 5, 250, len(controls) * line_height + 10)
    
 
    s = pygame.Surface((panel_rect[2], panel_rect[3]))
    s.set_alpha(180) 
    s.fill((0, 0, 0))
    surface.blit(s, (panel_rect[0], panel_rect[1]))

  
    for key, desc in controls:
    
        key_text = font.render(f"[{key}]", True, (255, 255, 0))
        
  
        desc_text = font.render(f" {desc}", True, (255, 255, 255))
        
        surface.blit(key_text, (x_pos, y_pos))
        surface.blit(desc_text, (x_pos + 50, y_pos))
        
        y_pos += line_height
    
