
"""
This file contains the biome placement and blending logic.
It implements the setup (on import) and
a function get_chunk_biome_map (at runtime). 
"""

import numpy as np
from enum import Enum
from scipy.ndimage import distance_transform_edt

import settings 

### Constants

# Biomes
N_BIOMES = 9 

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

BIOME_COLORS = np.array([
    [0.95, 0.95, 1.00],  # Tundra (Almost White/Snow)
    [0.05, 0.35, 0.25],  # Taiga (Dark Pine Green)
    [0.60, 0.75, 0.30],  # Temperate Grassland (Vibrant Light Green)
    [0.10, 0.60, 0.10],  # Temperate Forest (Standard Green)
    [0.05, 0.45, 0.15],  # Temperate Rainforest (Deep lush Green)
    [0.90, 0.85, 0.50],  # Subtropical Desert (Sand/Gold)
    [0.70, 0.75, 0.20],  # Savanna (Dry Yellow-Green)
    [0.30, 0.65, 0.10],  # Tropical Seasonal Forest (Bright Jungle Green)
    [0.05, 0.35, 0.10],  # Tropical Rainforest (Very Dark/Dense Green)
], dtype=np.float32)

assert(len(BIOME_COLORS) == N_BIOMES)



DTYPE = np.float32

### Whittaker map setup

def _build_whittaker_biome_map() -> np.ndarray:
    """
    Returns a (T, P) array with integer biome IDs.
    """
    biome_map = np.zeros(
        (settings.WHITTAKER_RES_T, settings.WHITTAKER_RES_P),
        dtype=np.uint8
    )
    t = np.linspace(0, 1, settings.WHITTAKER_RES_T)
    p = np.linspace(0, 1, settings.WHITTAKER_RES_P)
    T, P = np.meshgrid(t, p, indexing="ij")

    biome_map[:] = Biome.TEMPERATE_GRASSLAND.value
    biome_map[T < 0.25] = Biome.TUNDRA.value
    biome_map[(T < 0.4) & (P > 0.3)] = Biome.TAIGA.value  
    biome_map[(T >= 0.4) & (T < 0.7) & (P > 0.4)] = Biome.TEMPERATE_FOREST.value
    biome_map[(T >= 0.4) & (T < 0.7) & (P > 0.7)] = Biome.TEMPERATE_RAINFOREST.value
    biome_map[(T >= 0.7) & (P < 0.3)] = Biome.SUBTROPICAL_DESERT.value
    biome_map[(T >= 0.7) & (P >= 0.3) & (P < 0.6)] = Biome.SAVANNA.value
    biome_map[(T >= 0.7) & (P >= 0.6) & (P < 0.8)] = Biome.TROPICAL_SEASONAL_FOREST.value
    biome_map[(T >= 0.7) & (P >= 0.8)] = Biome.TROPICAL_RAINFOREST.value

    return biome_map



def _build_biome_weight_lut(biome_map: np.ndarray) -> np.ndarray:
    """
    Returns a (T, P, B) LUT with soft biome weights.
    """
    weights = np.zeros(
        (*biome_map.shape, N_BIOMES),
        dtype=DTYPE
    )

    if np.isscalar(settings.BIOME_SIGMA):
        sigmas = np.full(N_BIOMES, settings.BIOME_SIGMA, dtype=DTYPE)
    else:
        sigmas = np.asarray(settings.BIOME_SIGMA, dtype=DTYPE)

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


### Public function for biome mapping

def get_chunk_biome_map(
    precipitation: np.ndarray,
    temperature: np.ndarray
) -> np.ndarray:
    """
    Returns a (CHUNK_SIZE.x, CHUNK_SIZE.y, N_BIOMES) array.
    Each entry is a probability vector (sum = 1).
    """
    # Refactor: Ensure dimensions match settings.CHUNK_SIZE
    cx = int(settings.CHUNK_SIZE.x)
    cy = int(settings.CHUNK_SIZE.y)
    
    assert precipitation.shape == (cx, cy)
    assert temperature.shape == (cx, cy)
    
    # clamp just in case
    temperature = np.clip(temperature, 0.0, 1.0)
    precipitation = np.clip(precipitation, 0.0, 1.0)
    
    # map to LUT indices
    t_idx = (temperature * (settings.WHITTAKER_RES_T - 1)).astype(np.int16)
    p_idx = (precipitation * (settings.WHITTAKER_RES_P - 1)).astype(np.int16)

    biome_vectors = _BIOME_WEIGHT_LUT[t_idx, p_idx]

    return biome_vectors


### Public functions for biome colors

def biome_vectors_to_rgb(biome_vectors: np.ndarray) -> np.ndarray:
    """
    Converts (W, H, B) biome vectors into an RGB image via weighted color mixing.
    """
    assert biome_vectors.shape[-1] == N_BIOMES

    rgb = np.tensordot(
        biome_vectors,
        BIOME_COLORS,
        axes=([2], [0])
    )

    return rgb