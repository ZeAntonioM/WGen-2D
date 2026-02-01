# world/chunk.py
import pygame
import numpy as np
from pygame.math import Vector2

import settings
from world.utils import tile_to_world

# Imports from your generation package
from generation import noise_engine
from generation.biome_placement import get_chunk_biome_map, biome_vectors_to_rgb

from generation.climate_engine import ClimateEngine
from generation.wind_engine import WindEngine 

# --- INITIALIZE NOISE ENGINES ---
# We create these once so we don't re-init them for every chunk
ALTITUDE_NOISE_ENGINE = noise_engine.NoiseEngine(
    seed=settings.ALTITUDE_NOISE_SEED,
    frequency=settings.ALTITUDE_NOISE_FREQUENCY,
    fractal_octaves=settings.ALTITUDE_NOISE_OCTAVES
)
TEMPERATURE_NOISE_ENGINE = noise_engine.NoiseEngine(
    seed=settings.TEMPERATURE_NOISE_SEED,
    frequency=settings.TEMPERATURE_NOISE_FREQUENCY,
    fractal_octaves=settings.TEMPERATURE_NOISE_OCTAVES
)

# Initialize Wind
WIND_ENGINE = WindEngine(seed=settings.GLOBAL_SEED, scale=settings.WIND_SCALE)

# Initialize Climate
CLIMATE_ENGINE = ClimateEngine(ALTITUDE_NOISE_ENGINE, WIND_ENGINE)

class Chunk:
    def __init__(self, tile_pos: Vector2):
        self.tile_pos = tile_pos
        self.neighbors = dict()
        
        # New Environment Map storage
        self.env_maps = {
            "altitude": None,
            "temperature": None,
            "precipitation": None,
            "biomes": None
        }
        
        self.is_loaded = False
        self.surface = pygame.Surface(settings.CHUNK_SIZE)
        self._draw_surface()

    def get_corner_points(self) -> list[Vector2]:
        return [tile_to_world(self.tile_pos + Vector2(i, j)) for i, j in ((0, 0), (0, 1), (1, 0), (1, 1))]

    def load(self):
        if self.is_loaded: return
        self._create_neighbors()
        
        # 1. Generate Altitude
        # Note: We assume noise_engine.get_noise_height_map returns a numpy array
        self.env_maps["altitude"] = ALTITUDE_NOISE_ENGINE.get_noise_height_map(self.tile_pos.x, self.tile_pos.y)
        self._reshape_altitude() # Apply the polynomial curve
        
        # 2. Generate Temperature
        self.env_maps["temperature"] = TEMPERATURE_NOISE_ENGINE.get_noise_height_map(self.tile_pos.x, self.tile_pos.y)
        
        # 3. Calculate Derived Maps
        # TODO: Implement Wind-based precipitation here later!
        # For now, we just copy temperature as placeholder or use zeros
        self.env_maps["precipitation"] = CLIMATE_ENGINE.get_precipitation_map(
            self.tile_pos.x, 
            self.tile_pos.y
        )

        # 4. Biomes (This line stays the same, but now uses REAL precipitation!)
        self.env_maps["biomes"] = get_chunk_biome_map(
            self.env_maps["precipitation"], 
            self.env_maps["temperature"]
)
        
        self.is_loaded = True
        self._draw_surface()

    def unload(self):
        self.neighbors.clear()
        self.surface = None

    @property
    def position(self):
        return self.tile_pos

    def _draw_surface(self):
        """ 
        Visualizes the state of the chunk.
        If unloaded -> Red
        If loaded -> Biome Colors + Altitude Brightness
        """
        if not self.is_loaded:
            self.surface.fill((60, 40, 40))
            return
        
        a = self.env_maps["altitude"]
        WATER_LEVEL = 0.2 
        WATER_COLOR = [0.0, 0.1, 0.3]
        
        # Identify water pixels
        water_mask = a <= WATER_LEVEL

        if True:
            # Draw grayscale moisture map (Blueish)
            p = self.env_maps["precipitation"]
            # Convert 0-1 float to 0-255 RGB (Blue channel)
            p_viz = (p * 255).astype(np.uint8)
            
            # Create RGB array: (R=0, G=p, B=p) -> Cyan/Blue gradients
            zeros = np.zeros_like(p_viz)
            rgb = np.dstack((zeros, p_viz, p_viz)) 
            pygame.surfarray.blit_array(self.surface, rgb)
            return

        # Base colors from Biome Map
        biome_colors = biome_vectors_to_rgb(self.env_maps["biomes"])
        
        # Override water color
        # We divide by WATER_LEVEL to normalize brightness slightly
        biome_colors[water_mask] = np.array(WATER_COLOR) / WATER_LEVEL

        # Apply Altitude as brightness (Shadows/Highlights)
        # a[:, :, np.newaxis] adds a 3rd dimension so we can multiply RGB
        colors = biome_colors * a[:, :, np.newaxis]

        # Convert to Pygame format (0-255 uint8)
        pygame_colors = np.clip((colors * 255).astype(np.uint8), 0, 255)
        pygame.surfarray.blit_array(self.surface, pygame_colors)

    def _create_neighbors(self):
        # Local import to prevent circular dependency
        from world.chunk_manager import CHUNK_MANAGER
        
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                tile_pos = (self.position.x + x, self.position.y + y)
                if tile_pos in self.neighbors:
                    continue
                CHUNK_MANAGER.create_chunk(Vector2(*tile_pos))
                self.neighbors[tile_pos] = CHUNK_MANAGER.chunks[tile_pos]

    def _reshape_altitude(self):
        """ 
        Applies a polynomial function to make peaks peakier and plateaus flatter.
        """
        n = 1001 
        x_lut = np.linspace(0.0, 1.0, n)
        
        # The Magic Polynomial from the other developer
        y_lut = np.clip(
            - 0.0016371863
            - 2.219893 * x_lut
            + 23.44919786 * x_lut**2
            - 67.458179075828 * x_lut**3
            + 81.07774578363 * x_lut**4
            - 33.86123680241 * x_lut**5,
            0, 1
        )
        
        # Apply LUT using interpolation
        self.env_maps["altitude"] = np.interp(
            self.env_maps["altitude"], x_lut, y_lut
        )