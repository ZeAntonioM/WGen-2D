# world/utils.py
import math
from pygame.math import Vector2
import settings

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