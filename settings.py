# settings.py
import pygame
import warnings

# --- SCREEN & VISUALS ---
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
FPS = 60

# Colors
COLOR_BG = (20, 20, 20)
COLOR_GRID = (70, 70, 70)
COLOR_WIND = (100, 200, 255)
COLOR_PLAYER = (0, 0, 255)

# --- WORLD GENERATION BASE ---
GLOBAL_SEED = 123456
CHUNK_SIZE = pygame.Vector2(32, 32)
WIND_SCALE = 2000.0

# --- CHUNK LOADING ---
# Merged from simulation_const.py:
# DISTANCE_FOR_LOADING_CHUNKS -> LOAD_DISTANCE
# DISTANCE_FOR_UNLOADING_CHUNKS -> UNLOAD_DISTANCE
LOAD_DISTANCE = 200     # chunks inside this distance get loaded
UNLOAD_DISTANCE = 310   # chunks outside this distance get unloaded

# --- NOISE CONFIGURATION ---
# Merged from simulation_const.py

# Altitude
# We add an offset to the global seed so altitude looks different from other maps
ALTITUDE_NOISE_SEED = GLOBAL_SEED + 10 
ALTITUDE_NOISE_FREQUENCY = 0.0025 # lower means smoother terrain
ALTITUDE_NOISE_OCTAVES = 20       # higher means more jagged detail

# Temperature
TEMPERATURE_NOISE_SEED = GLOBAL_SEED + 11
TEMPERATURE_NOISE_FREQUENCY = 0.001
TEMPERATURE_NOISE_OCTAVES = 3

# --- VALIDATION CHECKS ---
# These ensure your configuration makes sense to prevent crashes later.

# 1. Loading buffer check
# We need a gap between loading and unloading to prevent "flickering" 
# (loading a chunk, unloading it immediately, then loading it again).
if not (LOAD_DISTANCE + 10 < UNLOAD_DISTANCE):
    raise AssertionError(f"UNLOAD_DISTANCE ({UNLOAD_DISTANCE}) must be significantly larger than LOAD_DISTANCE ({LOAD_DISTANCE})")

# 2. Chunk Size Integers
if not CHUNK_SIZE.x.is_integer() or not CHUNK_SIZE.y.is_integer():
    raise AssertionError("CHUNK_SIZE must use integer values.")

# 3. Square Chunk Warning
if CHUNK_SIZE.x != CHUNK_SIZE.y:
    warnings.warn("Non-square chunk sizes are not fully tested and may break logic.")


# --- BIOME SIMULATION ---
# Resolution of the Whittaker diagram LUT (Look Up Table)
# Higher = smoother gradients but slightly more memory usage (512x512 is standard)
WHITTAKER_RES_T = 512
WHITTAKER_RES_P = 512

# Softness of biome transitions (in LUT pixels)
# 1.0 = Sharp borders (Minecraft style)
# 20.0 = Soft blending (Realistic style)
BIOME_SIGMA = 20.0

WIND_SEED = 999
WIND_SCALE = 2000.0 # Controls how "large" the wind patterns are

# --- WATER & CLIMATE LEVELS ---
# The noise engine returns values from 0.0 to 1.0.
# Any altitude below 0.2 is considered Water/Ocean.
SEA_LEVEL = 0.2 

# Climate Physics
BASE_TEMP = 25.0        # Average global temperature
TEMP_LAPSE_RATE = 20.0  # Temperature drop per unit of altitude