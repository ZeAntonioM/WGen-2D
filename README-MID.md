# Procedural Generation of a Coherent Infinite 2D Landscape 
# --- Mid-Term Report ---

## Abstract (unchanged to initial project description)

This project explores procedural content generation of an infinite 2D top-down world using a chunk-based approach. The generated world is composed of different biomes, derived from multiple environmental maps (e.g., altitude, humidity, temperature), focusing on local and regional consistency and coherency. The goal is to study how noise-based algorithms mixed with rule-based decisions can produce large-scale worlds with smooth biome transitions and context-aware content placement.

## Progress Report

### Chunk system

The first progress in development has been the division of the infinite world into chunks of managable size. As large parts of the world remain unexplored, the chunks help in optimization by skipping generation and processing of such areas. With performance in mind, previously generated chunks will also be deleted if they fall out of render distance. Our deterministic generation approach ensures that chunks generate the same when revisiting a previously explored area.

However, the chunk system comes with a particular problem, that we needed to overcome. As we strive to produce coherent and believable generation of terrain, biomes and world content, the chunk borders could complicate the generation of large-scale features and could even render it impossible. As a solution, we made the neighboring chunks available during the generation process. In order to avoid infinite recursion of one chunk needing the next to properly generate, we introduced two states in which each chunk can be:
* A created chunk exists in code inside of our data structures and receives access to the local values of the environmental noise maps, as all chunks do. It does not try to load neighboring chunks.
* A loaded / generated chunk creates neighboring chunks to use for the generation. All of the generation, including biomes, water and other content, can be done without restriction. 

### Noise Engine and Environmental maps



## Changes to the initial plan

With the core foundations of the project implemented, it is time to review the initial plan and to adjust it if necessary. In our case, no changes to the project goal and procedure are needed, as the development until now adheres to the original plan. 

In the upcoming second half of the development phase, the following primary goals remain the same:
* Placement of coherent biomes based on environmental factors
* Biomes transition smoothly into neighboring biomes
* The generation will be deterministic, with a single, global seed
* All further content to be placed in the world are placed in a believable and context-aware manner


## Remaining tasks to complete

With every chunk having access to the environmental noise maps and its neighboring chunks, the generation of biomes, vegetation, bodies of water and other content can build on that. Regarding our very next step, which is the mapping of biomes, our procedure for implementing them consists of two phases and looks as follows:
* We introduce different types of biomes, each having a unique ruleset and lookup table. In this step, the raw noise data propagated to each chunk serves as the basis of decision for the placement of biomes.
* Due to the usage of hard rules, the transition will mirror this trend and be abrupt at first. The next step therefore is to blend different biomes that are located next to each other. It is critical in this step, that the neighbors of the currently generated chunk can be queried and taken into account, to ensure smooth biome blending at chunk borders.

Similarly, but not planned out in detail and fed as issues in small steps into our repository yet, is the placement of the remaining content of the world, in particular the water system (which mainly uses a threshold on an altitude map) and the vegetation, rocks and settlements (which are scattered based on probability distributions). 
