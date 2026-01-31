#!/usr/bin/python

"""
This file contains the biome placement and blending logic.
It implements the setup (on import) and
a function get_chunk_biome_map (at runtime). 
"""

import numpy as np
from enum import Enum
from scipy.ndimage import distance_transform_edt

CHUNK_SIZE = 512


### Constants

# Biomes
N_BIOMES = 9 # number

class Biome(Enum):
    TUNDRA = 0
    TAIGA = 1
    TEMPERATE_GRASSLAND = 2
    TEMPERATE_FOREST = 3
    TEMPERATE_RAINFOREST = 4
    SUBTROPICAL_DESERT = 5
    SAVANNA = 6
    TROPICAL_SEASONAL_FOREST = 7
    TROPICAL_RAINFOREST = 8
    #ALPINE = 9
    #OCEAN = 10

# Resolution of the Whittaker diagram LUT (look up table)
WHITTAKER_RES_T = 512
WHITTAKER_RES_P = 512

# Softness of biome transitions (in LUT pixels)
# Can be scalar or array of shape (N_BIOMES,)
BIOME_SIGMA = 5.0

DTYPE = np.float32



### Whittaker map setup

def _build_whittaker_biome_map() -> np.ndarray:
    """
    Returns a (T, P) array with integer biome IDs.
    """
    biome_map = np.zeros(
        (WHITTAKER_RES_T, WHITTAKER_RES_P),
        dtype=np.uint8
    )
    t = np.linspace(0, 1, WHITTAKER_RES_T)
    p = np.linspace(0, 1, WHITTAKER_RES_P)
    T, P = np.meshgrid(t, p, indexing="ij")

    biome_map[:] = Biome.TEMPERATE_GRASSLAND.value
    biome_map[T < 0.15] = Biome.TUNDRA.value
    biome_map[(T < 0.3) & (P > 0.4)] = Biome.TAIGA.value
    biome_map[(T > 0.3) & (T < 0.6) & (P > 0.4)] = Biome.TEMPERATE_FOREST.value
    biome_map[(T > 0.3) & (T < 0.6) & (P > 0.7)] = Biome.TEMPERATE_RAINFOREST.value
    biome_map[(T > 0.6) & (P < 0.25)] = Biome.SUBTROPICAL_DESERT.value
    biome_map[(T > 0.6) & (P > 0.25) & (P < 0.55)] = Biome.SAVANNA.value
    biome_map[(T > 0.6) & (P > 0.55) & (P < 0.8)] = Biome.TROPICAL_SEASONAL_FOREST.value
    biome_map[(T > 0.6) & (P > 0.8)] = Biome.TROPICAL_RAINFOREST.value

    return biome_map


### Setup LUT

def _build_biome_weight_lut(biome_map: np.ndarray) -> np.ndarray:
    """
    Builds a (T, P, B) LUT with soft biome weights.
    """

    weights = np.zeros(
        (*biome_map.shape, N_BIOMES),
        dtype=DTYPE
    )

    if np.isscalar(BIOME_SIGMA):
        sigmas = np.full(N_BIOMES, BIOME_SIGMA, dtype=DTYPE)
    else:
        sigmas = np.asarray(BIOME_SIGMA, dtype=DTYPE)

    for biome_id in range(N_BIOMES):
        mask = biome_map == biome_id

        # Distance to nearest pixel belonging to this biome
        dist = distance_transform_edt(~mask)

        sigma = sigmas[biome_id]
        weights[..., biome_id] = np.exp(
            -(dist ** 2) / (2.0 * sigma ** 2)
        )

    # Normalize to sum = 1
    weights /= weights.sum(axis=-1, keepdims=True)

    return weights


# runs once on import
_WHITTAKER_BIOME_MAP = _build_whittaker_biome_map()
_BIOME_WEIGHT_LUT = _build_biome_weight_lut(_WHITTAKER_BIOME_MAP)


### public function for biome mapping

def get_chunk_biome_map(
    altitude: np.ndarray,
    precipitation: np.ndarray,
    temperature: np.ndarray
) -> np.ndarray:
    """
    Returns a (CHUNK_SIZE, CHUNK_SIZE, N_BIOMES) array.
    Each entry is a probability vector (sum = 1).
    """
    assert altitude.shape == (CHUNK_SIZE, CHUNK_SIZE)
    assert precipitation.shape == (CHUNK_SIZE, CHUNK_SIZE)
    assert temperature.shape == (CHUNK_SIZE, CHUNK_SIZE)
    # clamp just in case
    temperature = np.clip(temperature, 0.0, 1.0)
    precipitation = np.clip(precipitation, 0.0, 1.0)
    # map to LUT indices
    t_idx = (temperature * (WHITTAKER_RES_T - 1)).astype(np.int16)
    p_idx = (precipitation * (WHITTAKER_RES_P - 1)).astype(np.int16)

    biome_vectors = _BIOME_WEIGHT_LUT[t_idx, p_idx]

    # altitude
    # water_mask = altitude < 0.2
    # biome_vectors[water_mask] *= 0.0
    # biome_vectors[water_mask, Biome.OCEAN] = 1.0
    # maybe Biome.ALPINE

    return biome_vectors
