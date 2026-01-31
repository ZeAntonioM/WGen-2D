""" Some sloppy code which opens a window, listens to keys to move the camera and shows the chunks
"""

import pygame
import chunk_management
from chunk_management import *

d = pygame.display.set_mode((1200, 600))

# create the grid 
grid = pygame.Surface(d.get_size()).convert_alpha()
grid.fill((0,0,0,0))
for x in range(int(grid.get_width()//CHUNK_SIZE.x)+1):
    pygame.draw.line(grid, (70, 70, 70), (x*CHUNK_SIZE.x, 0), (x*CHUNK_SIZE.x, grid.get_height()), 2)
for y in range(int(grid.get_height()//CHUNK_SIZE.y)+1):
    pygame.draw.line(grid, (70, 70, 70), (0, y*CHUNK_SIZE.y), (grid.get_width(), y*CHUNK_SIZE.y), 2)

camera_pos = Vector2(600, 300)
key_map = {direction: False for direction in ("left", "right", "up", "down")}

running = True
while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: key_map["left"] = True
            if event.key == pygame.K_RIGHT: key_map["right"] = True
            if event.key == pygame.K_UP: key_map["up"] = True
            if event.key == pygame.K_DOWN: key_map["down"] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: key_map["left"] = False
            if event.key == pygame.K_RIGHT: key_map["right"] = False
            if event.key == pygame.K_UP: key_map["up"] = False
            if event.key == pygame.K_DOWN: key_map["down"] = False
            
    #update
    if key_map["left"]: camera_pos.x -= 1
    if key_map["right"]: camera_pos.x += 1
    if key_map["up"]: camera_pos.y -= 1
    if key_map["down"]: camera_pos.y += 1
    CHUNK_MANAGER.update(camera_pos)
    
    # draw
    d.fill((0,0,0))
    for c in CHUNK_MANAGER.chunks.values():
        d.blit(c.surface, tile_to_world
               (c.position))
    pygame.draw.circle(d,(0, 0, 255), camera_pos, 4)
    #d.blit(grid, (0,0))
    
    pygame.display.update()
    
pygame.quit()
