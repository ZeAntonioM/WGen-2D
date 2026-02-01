import pygame
import math
import chunk_management
from chunk_management import *
from noise import snoise2

# --- 1. WIND ENGINE ---
class WindEngine:
    def __init__(self, seed=12345, scale=2000.0):
        self.scale = scale
        self.seed_x = seed
        self.seed_y = seed + 1000 

    def get_wind_at(self, x, y):
        nx = snoise2(x / self.scale, y / self.scale, octaves=2, base=self.seed_x)
        ny = snoise2(x / self.scale, y / self.scale, octaves=2, base=self.seed_y)
        return nx, ny

WIND_ENGINE = WindEngine(seed=42)

# --- 2. DRAWING FUNCTIONS ---

def draw_infinite_grid(surface, camera_pos):
    """ Draws grid lines aligned with chunk boundaries """
    screen_w, screen_h = surface.get_size()
    view_left = int(camera_pos.x - screen_w // 2)
    view_top = int(camera_pos.y - screen_h // 2)
    
    step_x = int(CHUNK_SIZE.x)
    step_y = int(CHUNK_SIZE.y)
    
    start_x = view_left - (view_left % step_x)
    start_y = view_top - (view_top % step_y)
    
    for world_x in range(start_x, view_left + screen_w + step_x, step_x):
        screen_x = world_x - view_left
        pygame.draw.line(surface, (70, 70, 70), (screen_x, 0), (screen_x, screen_h), 2)
        
    for world_y in range(start_y, view_top + screen_h + step_y, step_y):
        screen_y = world_y - view_top
        pygame.draw.line(surface, (70, 70, 70), (0, screen_y), (screen_w, screen_y), 2)

def draw_wind_arrows(surface, camera_pos, grid_spacing=64):
    screen_w, screen_h = surface.get_size()
    view_left = int(camera_pos.x - screen_w // 2)
    view_top = int(camera_pos.y - screen_h // 2)

    start_x = view_left - (view_left % grid_spacing)
    start_y = view_top - (view_top % grid_spacing)

    for x in range(start_x, view_left + screen_w + grid_spacing, grid_spacing):
        for y in range(start_y, view_top + screen_h + grid_spacing, grid_spacing):
            vx, vy = WIND_ENGINE.get_wind_at(x, y)
            screen_x = x - view_left
            screen_y = y - view_top

            arrow_len = 25
            mag = math.sqrt(vx**2 + vy**2)
            if mag == 0: continue
            
            end_x = screen_x + (vx / mag) * arrow_len
            end_y = screen_y + (vy / mag) * arrow_len
            
            color = (100, 200, 255) 
            pygame.draw.line(surface, color, (screen_x, screen_y), (end_x, end_y), 2)
            pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), 2)

# --- 3. MAIN SETUP ---
pygame.init()
d = pygame.display.set_mode((1200, 600))
screen_w, screen_h = d.get_size()

camera_pos = Vector2(0, 0)
key_map = {direction: False for direction in ("left", "right", "up", "down")}

# --- VISIBILITY FLAGS ---
# These control whether we draw the layers or not
show_wind = True   # Start visible (or set to False to start hidden)
show_grid = True   # Start visible

running = True
while running:
    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            
        if event.type == pygame.KEYDOWN:
            # Movement Keys
            if event.key == pygame.K_LEFT: key_map["left"] = True
            if event.key == pygame.K_RIGHT: key_map["right"] = True
            if event.key == pygame.K_UP: key_map["up"] = True
            if event.key == pygame.K_DOWN: key_map["down"] = True
            
            # --- TOGGLE KEYS ---
            if event.key == pygame.K_w:
                show_wind = not show_wind # Flip the boolean (True -> False, False -> True)
                print(f"Wind Visibility: {show_wind}") # Debug print
                
            if event.key == pygame.K_c: # I assume 'c' for Chunk Grid
                show_grid = not show_grid
                print(f"Grid Visibility: {show_grid}")
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: key_map["left"] = False
            if event.key == pygame.K_RIGHT: key_map["right"] = False
            if event.key == pygame.K_UP: key_map["up"] = False
            if event.key == pygame.K_DOWN: key_map["down"] = False
            
    # --- UPDATE ---
    move_speed = 10
    if key_map["left"]: camera_pos.x -= move_speed
    if key_map["right"]: camera_pos.x += move_speed
    if key_map["up"]: camera_pos.y -= move_speed
    if key_map["down"]: camera_pos.y += move_speed
    
    CHUNK_MANAGER.update(camera_pos)
    
    # --- DRAW ---
    d.fill((20, 20, 20))
    
    offset_x = camera_pos.x - (screen_w // 2)
    offset_y = camera_pos.y - (screen_h // 2)

    # 1. Draw Chunks (Always visible, unless you want a toggle for terrain too)
    for c in CHUNK_MANAGER.chunks.values():
        world_pos = tile_to_world(c.position)
        draw_pos = (world_pos[0] - offset_x, world_pos[1] - offset_y)
        d.blit(c.surface, draw_pos)
    
    # 2. Draw Grid (Only if flag is True)
    if show_grid:
        draw_infinite_grid(d, camera_pos)
    
    # 3. Draw Wind Arrows (Only if flag is True)
    if show_wind:
        draw_wind_arrows(d, camera_pos)
    
    # 4. Draw Player
    pygame.draw.circle(d, (0, 0, 255), (screen_w // 2, screen_h // 2), 8)
    
    pygame.display.update()
    
pygame.quit()