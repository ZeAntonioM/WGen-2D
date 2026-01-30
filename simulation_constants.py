#!/usr/bin/python

"""
This file contains all the important constants that this project uses.
Having them all in one place makes it easier to change consistently.
"""

import warnings
from pygame.math import Vector2

### Constants

#SEED = "123456" # not in use yet
CHUNK_SIZE = Vector2(32, 32)

# chunk loading
DISTANCE_FOR_LOADING_CHUNKS: int = 200 # chunks inside this distance get loaded
DISTANCE_FOR_UNLOADING_CHUNKS: int = 310 # chunks outside this distance get unloaded/deleted

# noise settings
ALTITUDE_NOISE_FREQUENCY = 0.0025 # lower means smoother
ALTITUDE_NOISE_OCTAVES = 20
TEMPERATURE_NOISE_FREQUENCY = 0.003
TEMPERATURE_NOISE_OCTAVES = 5


### Asserts and warnings about constants
assert(DISTANCE_FOR_LOADING_CHUNKS+10 < DISTANCE_FOR_UNLOADING_CHUNKS)
assert(CHUNK_SIZE.x.is_integer())
assert(CHUNK_SIZE.y.is_integer())
if CHUNK_SIZE.x != CHUNK_SIZE.y:
    warnings.warn("non-square chunk sizes are not fully tested and may break")
