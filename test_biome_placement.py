#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

from simulation_constants import CHUNK_SIZE
from biome_placement import get_chunk_biome_map, N_BIOMES, biome_vectors_to_rgb


# ============================================================
# Test chunk generation
# ============================================================

def generate_test_chunk():
    """
    altitude:      constant 0
    temperature:   increases from left (0) to right (1)
    precipitation: increases from bottom (0) to top (1)
    """

    altitude = np.zeros((int(CHUNK_SIZE.x), int(CHUNK_SIZE.y)), dtype=np.float32)

    temperature = np.linspace(
        0.0, 1.0, int(CHUNK_SIZE.y), dtype=np.float32
    )[None, :].repeat(int(CHUNK_SIZE.x), axis=0)

    precipitation = np.linspace(
        0.0, 1.0, int(CHUNK_SIZE.y), dtype=np.float32
    )[:, None].repeat(int(CHUNK_SIZE.x), axis=1)

    return altitude, precipitation, temperature


# ============================================================
# Main
# ============================================================

def main():
    altitude, precipitation, temperature = generate_test_chunk()

    biome_vectors = get_chunk_biome_map(
        #altitude=altitude,
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
