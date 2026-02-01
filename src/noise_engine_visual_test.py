#!/usr/bin/python

"""
This test should show a red background with black and white noise on top
The topleft chunk is drawn in blue for scale.
The chunk (3, 4) is missing on purpose.
"""

import pygame
from noise_engine import *
import numpy as np
from simulation_constants import *


ne = NoiseEngine(seed=13426356)

display = pygame.display.set_mode((1000, 500))
display.fill((100, 0, 0))

def array_to_surface(a: np.array) -> pygame.Surface:
    s = pygame.Surface((CHUNK_SIZE.x, CHUNK_SIZE.y))
    s.fill((0, 255, 255))
    color = [a[0, 0]*255]*3
    for x in range(int(CHUNK_SIZE.x)):
        for y in range(int(CHUNK_SIZE.y)):
            color = [a[x, y]*255]*3
            s.set_at((x, y), color)
    return s

for x in range(0, int(1000 / CHUNK_SIZE.x)):
    for y in range(0, int(500 / CHUNK_SIZE.y)):
        if x == 3 and y == 4:
            continue
        a = ne.get_noise_height_map(x, y)
        s = array_to_surface(a)
        display.blit(s, (x*CHUNK_SIZE.x, y*CHUNK_SIZE.y))

pygame.draw.rect(display, (0, 0, 255), ((0, 0), CHUNK_SIZE), 1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
    
pygame.quit()
