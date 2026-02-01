# settings.py
import pygame
import warnings

# Import everything from the split files
# This allows 'import settings' to work exactly as it did before
from app_settings import *
from simulation_settings import *

# --- VALIDATION CHECKS ---
# We keep these here to ensure the combined settings are valid.

# 1. Loading buffer check
if not (LOAD_DISTANCE + 10 < UNLOAD_DISTANCE):
    raise AssertionError(f"UNLOAD_DISTANCE ({UNLOAD_DISTANCE}) must be significantly larger than LOAD_DISTANCE ({LOAD_DISTANCE})")

# 2. Chunk Size Integers
if not CHUNK_SIZE.x.is_integer() or not CHUNK_SIZE.y.is_integer():
    raise AssertionError("CHUNK_SIZE must use integer values.")

# 3. Square Chunk Warning
if CHUNK_SIZE.x != CHUNK_SIZE.y:
    warnings.warn("Non-square chunk sizes are not fully tested and may break logic.")