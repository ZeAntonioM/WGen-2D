# world/utils.py
import math
from pygame.math import Vector2
import numpy as np
import settings
import time

def world_to_tile(world_pos: Vector2) -> Vector2:
    return Vector2(
        int(round(world_pos.x / settings.CHUNK_SIZE.x)), 
        int(round(world_pos.y / settings.CHUNK_SIZE.y))
    )

def tile_to_world(tile_pos: Vector2) -> Vector2:
    return Vector2(
        tile_pos.x * settings.CHUNK_SIZE.x, 
        tile_pos.y * settings.CHUNK_SIZE.y
    )

def distance_to_chunk_center(pos: Vector2, tile_pos: Vector2) -> float:
    center = tile_to_world(tile_pos) + settings.CHUNK_SIZE / 2
    return pos.distance_to(center)


def apply_function_to_map(function, map_: np.array, sampling_steps=1001) -> np.array:
    """
    Applies the given function [0,1] -> [0,1] to the map_ of shape (x, y) efficiently.
    It uses sampling to create look up tables and uses linear interpolation.
    Returns the new map.
    """
    x_lut = np.linspace(0.0, 1.0, sampling_steps)
    y_lut = np.clip(function(x_lut), 0, 1)
    return np.interp(map_, x_lut, y_lut)

class LagReducer():
    
    def __init__(self, strength:int=1):
        self._counter = 0
        assert(strength <= 1000)
        self._max_count = round(1000/strength)
        assert(self._max_count >= 1)
    
    def reduce_lag(self):
        """
        Call this function inside a loop that produces lag by being called VERY often.
        It gives the activity to the main thread, so that the main thread runs smoothly.
        (at the expense of this function taking some additional time).
        Only works with multithreading enabled
        """
        if not settings.USE_MULTITHREADING:
            return
        self._counter += 1
        if self._counter >= self._max_count:
            self._counter = 0
            time.sleep(0.01)
