# Procedural Generation of a Coherent Infinite 2D Landscape

## Abstract

This project explores procedural content generation of an infinite 2D top-down world using a chunk-based approach. The generated world is composed of different biomes, derived from multiple environmental maps (e.g., altitude, humidity, temperature), focusing on local and regional consistency and coherency. The goal is to study how noise-based algorithms mixed with rule-based decisions can produce large-scale worlds with smooth biome transitions and context-aware content placement.

## Background and Motivation

Many games rely on procedural content generation to create large worlds that feel coherent and structured, rather than purely random. While different games adopt different approaches, they often share the same underlying goal: ensuring that the generated world makes sense according to its own internal rules.

For example, Minecraft generates vast worlds composed of varied biomes that transition in a consistent and recognizable way, while RimWorld divides its world into multiple regions that may repeat biomes or patterns yet still remain coherent within the game’s logic. These worlds do not necessarily follow real-world planetary rules, but they maintain internal consistency that makes them believable and playable.

Observing how such games balance repetition, large-scale structure, and local detail motivated us to explore similar ideas in a simplified setting. This project focuses on understanding how coherence can be preserved in an infinite, procedurally generated world, using relatively simple mechanisms such as continuous noise fields and rule-based decisions, without relying on full global simulation.

## Project Goal

Beyond basic terrain generation, the project aims to explicitly address coherence in infinite worlds without full global precomputation, regarding the generation of biomes and content placement. The generator is designed so that all properties (biomes, water proximity, content placement) are derived from continuous global fields that can be queried locally, removing the need to remember old chunks.

The main goal of this project is to design and implement a procedural generator for an infinite 2D top-down world that:

* Produces coherent biomes based on environmental factors
* Supports smooth transitions between neighboring biomes
* Allows deterministic generation using a single, global seed
* Places world content (e.g., vegetation, rocks, water, settlements) in a context-aware manner

The final output of the project is expected to be a simple visual representation of the generated world using pygame, along with analysis and discussion of different methods of generating coherent infinite worlds.

## Methodology

As said before, the world will be generated using a chunk-based approach, where the infinite map is divided into fixed-size chunks. Each chunk is generated deterministically from a global seed combined with its coordinates, ensuring consistency if the user revisits the same chunk.

Generation is structured in multiple layers:

1. **Environmental Maps**  
   Different continuous noise functions (e.g., Perlin or Simplex noise) are used to generate underlying environmental fields such as altitude, humidity, and temperature. These maps are defined in world space and can be queried at arbitrary coordinates without requiring full world generation.

   To enable analysis and comparison, different configurations will be available to users, such as:
   - Single noise vs. multiple independent noise maps
   - Different noise frequencies (low-frequency vs. multi-octave noise using fractal Brownian)
   - Correlated vs. uncorrelated environmental maps, to study their effects on biome distribution and coherence.

2. **Biomes**  
   Biomes are derived from combinations of environmental values using rule-based thresholds or weighted conditions. Instead of assigning a single biome per tile with hard borders, biome influences are blended near boundaries, allowing tiles to be partially influenced by multiple biomes and reducing abrupt transitions.

3. **Water bodies**  
   Water bodies (e.g., seas or lakes) are mainly derived from altitude. From these, distance-to-water values can be computed and used as an additional environmental factor influencing biome selection. This approach allows water-related properties to be queried locally without explicit global knowledge.

4. **Context-Aware Content Placement**  
   World elements such as trees, rocks, and settlements are placed according to local biome type and environmental conditions (e.g., vegetation density being influenced by humidity). These rules are simple but designed to produce believable large-scale patterns.

The project doesn't aim to reproduce planetary-scale climate simulation. Instead, the coherence emerges from consistent rules applied over continuous global fields, allowing for infinite expansion while keeping the system analyzable and computationally possible.
The project will be implemented in Python, utilizing libraries such as NumPy for numerical computations and Pygame for visualization. The code will be modular to allow easy experimentation with different noise functions, biome rules, and content placement strategies.