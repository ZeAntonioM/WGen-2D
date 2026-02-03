# main.py
import pygame
import settings
import graphics.visuals as visuals
from world.utils import tile_to_world
from world.chunk_manager import ChunkManager
from generation.generator import Generator

def menu(display, clock):
    
    input_text = ""
    font_title = pygame.font.SysFont("arial", 50, bold=True)
    font_text = pygame.font.SysFont("consolas", 30)
    
    menu_running = True
    
    while menu_running:
        display.fill((30, 30, 30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text == "":
                        return 12345 
                    return string_to_seed(input_text)
                
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    if len(input_text) < 15:
                        input_text += event.unicode

        title_surf = font_title.render("Procedural Generation of a Coherent Infinite 2D", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))
        display.blit(title_surf, title_rect)

        instr_surf = font_text.render("Write down the seed for your world:", True, (200, 200, 200))
        instr_rect = instr_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 30))
        display.blit(instr_surf, instr_rect)

        input_box = pygame.Rect(0, 0, 400, 50)
        input_box.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 30)
        pygame.draw.rect(display, (255, 255, 255), input_box, 2) # Borda
        
        text_surf = font_text.render(input_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=input_box.center)
        display.blit(text_surf, text_rect)
        
        note_surf = font_text.render("(Leave empty for default)", True, (100, 100, 100))
        note_rect = note_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 80))
        display.blit(note_surf, note_rect)

        pygame.display.update()
        clock.tick(30)

def string_to_seed(s):
    if s.lstrip().isdigit():
        return int(s)
    
    val = 0
    for char in s:
        val = (val * 31 + ord(char)) & 0xFFFFFFFF

    if val > 0x7FFFFFFF:
        val -= 0x100000000
        
    return val


def main():
    pygame.init()
    display = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    user_seed = menu(display, clock)
    print(f"Seed chosen: {user_seed}")

    generator = Generator(user_seed)
    chunk_manager = ChunkManager(generator)
    
    camera_pos = pygame.Vector2(0, 0)
    key_map = {key: False for key in ("left", "right", "up", "down")}

    # Visibility Flags
    show_wind = False
    show_grid = False
    
    view_mode = "biomes" 
    
    running = True
    while running:
        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                               
            if event.type == pygame.VIDEORESIZE:
                settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT = event.w, event.h
                pygame.display.update() 
            
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
                if event.key == pygame.K_5: new_mode = "river"
                
                if new_mode and new_mode != view_mode:
                    view_mode = new_mode
                    print(f"Switching view to: {view_mode}")
                    for chunk in chunk_manager.chunks.values():
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
        chunk_manager.update(camera_pos)

        if view_mode != "biomes":
             for chunk in chunk_manager.chunks.values():
                 chunk.update_graphics(view_mode)

        # --- DRAW ---
        display.fill(settings.COLOR_BG)
        
        offset_x = camera_pos.x - (settings.SCREEN_WIDTH // 2)
        offset_y = camera_pos.y - (settings.SCREEN_HEIGHT // 2)

        # 1. Draw Chunks (Content)
        for c in chunk_manager.chunks.values():
            world_pos = tile_to_world(c.position)
            draw_pos = (world_pos[0] - offset_x, world_pos[1] - offset_y)
            display.blit(c.surface, draw_pos)
        
        # 2. Draw Visuals (Presentation)
        if show_grid:
            visuals.draw_infinite_grid(display, camera_pos, settings.CHUNK_SIZE)
        
        if show_wind:
            visuals.draw_wind_arrows(display, camera_pos, generator.wind_engine)
        
        # 3. Draw Player
        center_screen = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
        pygame.draw.circle(display, settings.COLOR_PLAYER, center_screen, 8)

        visuals.draw_controls_hud(display)

        pygame.display.update()
        clock.tick(settings.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
