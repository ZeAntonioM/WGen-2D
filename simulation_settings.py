import pygame 

# --- WORLD GENERATION BASE ---
GLOBAL_SEED = 123456
CHUNK_SIZE = pygame.Vector2(32, 32)
WIND_SEED = 999
WIND_SCALE = 2000.0

# --- NOISE CONFIGURATION ---
# Altitude
ALTITUDE_NOISE_SEED = GLOBAL_SEED + 10 
ALTITUDE_NOISE_FREQUENCY = 0.0025 
ALTITUDE_NOISE_OCTAVES = 20       

# Temperature
TEMPERATURE_NOISE_SEED = GLOBAL_SEED + 11
TEMPERATURE_NOISE_FREQUENCY = 0.001
TEMPERATURE_NOISE_OCTAVES = 3

# --- BIOME SIMULATION ---
WHITTAKER_RES_T = 512
WHITTAKER_RES_P = 512
BIOME_SIGMA = 20.0 # Soft blending

# --- WATER & CLIMATE LEVELS ---
SEA_LEVEL = 0.2 
BASE_TEMP = 25.0        
TEMP_LAPSE_RATE = 20.0  

# --- CLIMATE SIMULATION ---
MAX_STEPS = 60          # Bigger -> more precise, slower
STEP_SIZE = 16.0        # Bigger -> Faster, less precise
CLIMATE_STEP = 4        # Bigger -> less detail, faster   

# Physics
MOISTURE_PICKUP = 0.05  # Moisture gain on water
DECAY_ON_LAND = 0.02    # constant moisture cost on land
MOUNTAIN_COST = 1       # Cost on moisture from passing throught a mountain
=======
MAX_STEPS = 80          # Bigger -> more precise, slower
STEP_SIZE = 4        # Bigger -> Faster, less precise
CLIMATE_STEP = 4        # Bigger -> less detail, faster   

# Physics
MOISTURE_PICKUP = 1  # Moisture gain on water
DECAY_ON_LAND = 0    # constant moisture cost on land
MOUNTAIN_COST = 10       # Cost on moisture from passing throught a mountain
>>>>>>> Stashed changes
