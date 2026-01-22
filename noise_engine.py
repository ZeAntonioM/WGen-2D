#!/usr/bin/python

"""
First template for the noise engine

"""

from collections.abc import Callable


class NoiseEngine():
    
    def __init__(self):
        pass

    def get_2d_noise_map(self) -> Callable[[Vector2], float]:
        """ Returns a 2d noise map that can be called at any world coordinate (pygame.math.Vector2)
        and returns a float value between 0 and 1 """
        raise NotImplementedError()
        def noise_map(pos: Vector2) -> float:
            return 0.0
        return noise_map

    
