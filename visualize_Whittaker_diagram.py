#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pygame

import settings
from generation.biome_placement import get_chunk_biome_map, N_BIOMES, biome_vectors_to_rgb

settings.CHUNK_SIZE = pygame.Vector2(100, 100)
CHUNK_SIZE = settings.CHUNK_SIZE

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
        altitude=altitude,
        precipitation=precipitation,
        temperature=temperature
    )

    rgb = biome_vectors_to_rgb(biome_vectors)

    plt.figure(figsize=(6, 6))
    plt.imshow(rgb, origin="lower")
    #plt.title("Whittaker Diagram")
    plt.xlabel("Temperature", fontsize=18, labelpad=10)
    plt.ylabel("Precipitation", fontsize=18, labelpad=10)

    # text
    font_dict = {
        "fontsize": 18,
        "horizontalalignment": "center",
        "verticalalignment": "center_baseline"
    }
    for xpos, ypos, labeltext in (
        (12.5, 50, "Tundra"),
        (32.5, 65, "Taiga"),
        (55, 85, "Temperate\nrainforest"),
        (55, 55, "Temperate\nforest"),
        (85, 90, "Tropical\nrainforest"),
        (85, 70, "Tropical\nseasonal\nforest"),
        (85, 45, "Savanna"),
        (85, 15, "Subtropical\ndesert"),
        (47.5, 20, "Grassland")
    ):
        pass#plt.text(xpos, ypos, " \n".join(labeltext.split("\n"))+" ", **font_dict)
    
    # only ticks at boundaries:
    plt.xticks((0, 25, 40, 70, 100), [round(x/100, 2) for x in (0, 25, 40, 70, 100)], fontsize=15)
    plt.yticks((0, 30, 40, 60, 70, 80, 100), [round(x/100, 2) for x in (0, 30, 40, 60, 70, 80, 100)], fontsize=15)

    # regular ticks
    #plt.xticks(range(0, 100+1, 10), [round(x/100, 2) for x in range(0, 100+1, 10)])
    #plt.yticks(range(0, 100+1, 10), [round(x/100, 2) for x in range(0, 100+1, 10)])
    
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig('wd.png', dpi=200) #default dpi=100
    #plt.show()


if __name__ == "__main__":
    main()
