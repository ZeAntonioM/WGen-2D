import pygame
from generation.noise_engine import *
import numpy as np


ne = NoiseEngine(seed=13426356)

display = pygame.display.set_mode((1000, 500))
display.fill((100, 0, 0))

chunk_size = ne.chunk_size

def array_to_surface(a: np.array) -> pygame.Surface:
    s = pygame.Surface((chunk_size, chunk_size))
    s.fill((0, 255, 255))
    color = [a[0, 0]*255]*3
    for x in range(chunk_size):
        for y in range(chunk_size):
            color = [a[x, y]*255]*3
            s.set_at((x, y), color)
    return s

for x in range(0, int(1000 / chunk_size)):
    for y in range(0, int(500 / chunk_size)):
        a = ne.get_noise_height_map(x, y)
        s = array_to_surface(a)
        display.blit(s, (x*chunk_size, y*chunk_size))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
    
pygame.quit()
