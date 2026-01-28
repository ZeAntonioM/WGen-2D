# WGen-2D

## Noise Engine

### Overview
`NoiseEngine` is a singleton class that provides noise maps for procedural generation. It uses a Cython wrapper for FastNoiseLite called `pyfastnoiselite` to generate the noise for the terrain generation.
The `NoiseEngine` class uses OpenSimplex2 noise by default. It is the commonly used noise type for terrain generation due to its smoothness and natural appearance and a direct evolution of Simplex noise. The library also supports other noise types like Perlin, Cellular, and Value noise, as well as a simplex noise variant called OpenSimplex2S.
For the fractal type, the default is set to FBM (Fractional Brownian Motion), which combines multiple layers of noise to create more complex and detailed patterns. Other fractal types supported include Ridged, PingPong, and DomainWarp.

### Features
Currently supports seed customization and frequency adjustment. 
If needed, the class also extends support for different noise types and fractal types. 
Its only method, get_noise_height_map, receives the world coordinates and returns a 2D numpy array representing the height map, with values normalized between 0 and 1 that can be adapted for different purposes like terrain elevation, texture mapping, etc.

### Usage
```python
from noise_engine import NoiseEngine
noise_engine = NoiseEngine(seed=42, frequency=0.01)
height_map = noise_engine.get_noise_height_map(x_start=0, y_start=0)
```


