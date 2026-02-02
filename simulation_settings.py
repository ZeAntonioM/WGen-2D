import pygame 

# --- WORLD GENERATION BASE ---
GLOBAL_SEED = 123456
CHUNK_SIZE = pygame.Vector2(32, 32)

# --- NOISE CONFIGURATION ---
# Altitude
ALTITUDE_NOISE_SEED = GLOBAL_SEED + 10 
ALTITUDE_NOISE_FREQUENCY = 0.0025 
ALTITUDE_NOISE_OCTAVES = 20
ALTITUDE_RESHAPING_FUNCTION = lambda x: \
    - 0.0016371863 \
    - 2.219893 * x \
    + 23.44919786 * x**2 \
    - 67.458179075828 * x**3 \
    + 81.07774578363 * x**4 \
    - 33.86123680241 * x**5

# Temperature
TEMPERATURE_NOISE_SEED = GLOBAL_SEED + 11
TEMPERATURE_NOISE_FREQUENCY = 0.001
TEMPERATURE_NOISE_OCTAVES = 3

# Wind
WIND_SEED = GLOBAL_SEED + 12
WIND_SCALE = 2000.0

# --- BIOME SIMULATION ---
WHITTAKER_RES_T = 512
WHITTAKER_RES_P = 512
BIOME_SIGMA = 20.0 # Soft blending

# --- WATER & CLIMATE LEVELS ---
SEA_LEVEL = 0.2
WATER_LEVEL_RESHAPING_FUNCTION = lambda x: \
    - 0.24738095238096944 * x \
    + 3.063214285714324 * x**2 \
    - 4.527976190476227 * x**3 \
    + 1.9821428571428705 * x**4
BASE_TEMP = 25.0        
TEMP_LAPSE_RATE = 20.0  

# --- CLIMATE SIMULATION ---
MAX_STEPS = 40          # Bigger -> more precise, slower
STEP_SIZE = 3        # Bigger -> Faster, less precise
CLIMATE_STEP = 4        # Bigger -> less detail, faster   

# Physics
MOISTURE_PICKUP = 1  # Moisture gain on water
DECAY_ON_LAND = 0    # constant moisture cost on land
MOUNTAIN_COST = 5       # Cost on moisture from passing throught a mountain
