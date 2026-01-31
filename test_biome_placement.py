#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

from biome_placement import CHUNK_SIZE
from biome_placement import get_chunk_biome_map, N_BIOMES


# ============================================================
# Test chunk generation
# ============================================================

def generate_test_chunk():
    """
    altitude:      constant 0
    temperature:   increases from left (0) to right (1)
    precipitation: increases from bottom (0) to top (1)
    """

    altitude = np.zeros((CHUNK_SIZE, CHUNK_SIZE), dtype=np.float32)

    temperature = np.linspace(
        0.0, 1.0, CHUNK_SIZE, dtype=np.float32
    )[None, :].repeat(CHUNK_SIZE, axis=0)

    precipitation = np.linspace(
        0.0, 1.0, CHUNK_SIZE, dtype=np.float32
    )[:, None].repeat(CHUNK_SIZE, axis=1)

    return altitude, precipitation, temperature


# ============================================================
# Biome colors (DEBUG / VISUALIZATION ONLY)
# ============================================================

BIOME_COLORS = np.array([
    [0.80, 0.80, 0.90],  # Tundra
    [0.40, 0.60, 0.20],  # Taiga
    [0.80, 0.80, 0.30],  # Temperate grassland
    [0.30, 0.70, 0.30],  # Temperate forest
    [0.10, 0.50, 0.30],  # Temperate rainforest
    [0.90, 0.80, 0.30],  # Subtropical desert
    [0.70, 0.70, 0.20],  # Savanna
    [0.20, 0.80, 0.30],  # Tropical seasonal forest
    [0.10, 0.60, 0.10],  # Tropical rainforest
    #[0.60, 0.60, 0.60],  # Alpine / extra
], dtype=np.float32)


# ============================================================
# Visualization
# ============================================================

def biome_vectors_to_rgb(biome_vectors: np.ndarray) -> np.ndarray:
    """
    Converts (H, W, B) biome vectors into an RGB image via weighted color mixing.
    """

    assert biome_vectors.shape[-1] == N_BIOMES

    rgb = np.tensordot(
        biome_vectors,
        BIOME_COLORS,
        axes=([2], [0])
    )

    return np.clip(rgb, 0.0, 1.0)


# ============================================================
# Main
# ============================================================

def main():
    altitude, precipitation, temperature = generate_test_chunk()

    biome_vectors = get_chunk_biome_map(
        altitude=altitude,
        precipitation=precipitation,
        temperature=temperature
    )

    rgb = biome_vectors_to_rgb(biome_vectors)

    plt.figure(figsize=(6, 6))
    plt.imshow(rgb, origin="lower")
    plt.title("Biome Placement Test (Whittaker Diagram)")
    plt.xlabel("Temperature →")
    plt.ylabel("Precipitation ↑")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
