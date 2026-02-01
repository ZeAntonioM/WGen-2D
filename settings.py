# settings.py
import pygame

# Screen Settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

# World Generation
GLOBAL_SEED = 42
WIND_SCALE = 2000.0

# Colors
COLOR_BG = (20, 20, 20)
COLOR_GRID = (70, 70, 70)
COLOR_WIND = (100, 200, 255)
COLOR_PLAYER = (0, 0, 255)

# Chunk Settings (If you don't already have them in chunk_management)
CHUNK_SIZE = pygame.Vector2(32 * 16, 32 * 16) # Example