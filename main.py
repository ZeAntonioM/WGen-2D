# main.py
import pygame
import settings
import graphics.visuals as visuals
from world.chunk_manager import CHUNK_MANAGER
from world.utils import tile_to_world
from generation.wind_engine import WindEngine
from generation.engine_singletons import *

def main():
    pygame.init()
    display = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    wind_engine = WindEngine(seed=settings.WIND_SEED, scale=settings.WIND_SCALE)
    
    camera_pos = pygame.Vector2(0, 0)
    key_map = {key: False for key in ("left", "right", "up", "down")}

    # Visibility Flags
    show_wind = True
    show_grid = True
    
    view_mode = "biomes" 
    
    running = True
    while running:
        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: key_map["left"] = True
                if event.key == pygame.K_RIGHT: key_map["right"] = True
                if event.key == pygame.K_UP: key_map["up"] = True
                if event.key == pygame.K_DOWN: key_map["down"] = True
                
                # Toggles
                if event.key == pygame.K_w: show_wind = not show_wind
                if event.key == pygame.K_c: show_grid = not show_grid

                # --- DEBUG VIEW MODES ---
                new_mode = None
                if event.key == pygame.K_1: new_mode = "biomes"
                if event.key == pygame.K_2: new_mode = "altitude"
                if event.key == pygame.K_3: new_mode = "temperature"
                if event.key == pygame.K_4: new_mode = "precipitation"
                
                if new_mode and new_mode != view_mode:
                    view_mode = new_mode
                    print(f"Switching view to: {view_mode}")
                    for chunk in CHUNK_MANAGER.chunks.values():
                        chunk.update_graphics(view_mode)

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
        
        # Update Content (Loads/Unloads chunks)
        CHUNK_MANAGER.update(camera_pos)

        if view_mode != "biomes":
             for chunk in CHUNK_MANAGER.chunks.values():
                 chunk.update_graphics(view_mode)

        # --- DRAW ---
        display.fill(settings.COLOR_BG)
        
        offset_x = camera_pos.x - (settings.SCREEN_WIDTH // 2)
        offset_y = camera_pos.y - (settings.SCREEN_HEIGHT // 2)

        # 1. Draw Chunks (Content)
        for c in CHUNK_MANAGER.chunks.values():
            world_pos = tile_to_world(c.position)
            draw_pos = (world_pos[0] - offset_x, world_pos[1] - offset_y)
            display.blit(c.surface, draw_pos)
        
        # 2. Draw Visuals (Presentation)
        if show_grid:
            visuals.draw_infinite_grid(display, camera_pos, settings.CHUNK_SIZE)
        
        if show_wind:
            visuals.draw_wind_arrows(display, camera_pos, wind_engine)
        
        # 3. Draw Player
        center_screen = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
        #pygame.draw.circle(display, settings.COLOR_PLAYER, center_screen, 8)

        pygame.display.update()
        clock.tick(settings.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
