<div align="center">
<h1>Procedural Generation of a Coherent Infinite 2D Landscape<br> -&nbsp;&nbsp;Mid-Term Report&nbsp;&nbsp;- </h1>
</div>

## Abstract (unchanged to initial project description)

This project explores procedural content generation of an infinite 2D top-down world using a chunk-based approach. The generated world is composed of different biomes, derived from multiple environmental maps (e.g., altitude, humidity, temperature), focusing on local and regional consistency and coherency. The goal is to study how noise-based algorithms mixed with rule-based decisions can produce large-scale worlds with smooth biome transitions and context-aware content placement.

## Progress Report

### Project Planning on GitHub

From the beginning of the project, we have been using GitHub to plan and track our progress. First, a meeting was held to outline the project steps and to break them down into more manageable tasks. After that, issues were created in the repository to represent these tasks and explain them in detail. Each issue contains a description of the task, its goals, and acceptance criteria. As we progressed, we continuously updated the issues, marking them as completed when done and creating new ones as needed. This approach has helped us to stay organized and focused on our objectives. There are currently 7 issues in total, which may increase as we proceed with the development. These issues can be found in the [Issues](https://github.com/ZeAntonioM/WGen-2D/issues) section of our GitHub repository. Finally, we have been using pull requests to review and merge changes into the main codebase, ensuring that all contributions are properly examined and integrated. 


### Chunk system

The first and major progress in development has been the division of the infinite world into chunks of managable size. As large parts of the world remain unexplored, the chunks help in optimization by skipping generation and processing of such areas. With performance in mind, previously generated chunks will also be deleted if they fall out of render distance. Our deterministic generation approach ensures that chunks generate the same when revisiting a previously explored area.

However, the chunk system comes with a particular problem, that we needed to overcome. As we strive to produce coherent and believable generation of terrain, biomes and world content, the chunk borders could complicate the generation of large-scale features and could even render it impossible. As a solution, we made the neighboring chunks available during the generation process. In order to avoid infinite recursion of one chunk needing the next to properly generate, we introduced two states in which each chunk can be:
* A created chunk exists in code inside of our data structures and receives access to the local values of the environmental noise maps, as all chunks do. It does not try to load neighboring chunks.
* A loaded / generated chunk creates neighboring chunks to use for the generation. All of the generation, including biomes, water and other content, can be done without restriction. 

### Noise Engine and Environmental maps

The next major step in our development will be the implementation of the environmental noise maps. We are currently making the research and evaluation of different noise algorithms, to find the best fit for the project. The actual implementation of the is currently in ongoing development.

## Changes to the initial plan

With the core foundations of the project implemented, it is time to review the initial plan and to adjust it if necessary. In our case, no changes to the project goal and procedure are needed, as the development until now adheres to the original plan. 

In the upcoming second half of the development phase, the following primary goals remain the same:
* Placement of coherent biomes based on environmental factors
* Biomes transition smoothly into neighboring biomes
* The generation will be deterministic, with a single, global seed
* All further content to be placed in the world are placed in a believable and context-aware manner


## Remaining tasks to complete

- [Issue #1](https://github.com/ZeAntonioM/WGen-2D/issues/1): In order to have a foundation for the generation of biomes, vegetation and other world content, we need to finish the implementation of the noise engine to provide each point in the world with random noise to build the content generation upon. 

- [Issue #3](https://github.com/ZeAntonioM/WGen-2D/issues/3): The following step is connecting the new noise engine to the existing chunk system, so that a chunk can query the noise in the form of meaningful environment maps during the generation process. This way, we have a solid foundation for the upcoming generation. With every chunk having access to the environmental noise maps and its neighboring chunks, the generation of biomes, vegetation, bodies of water and other content can build on that.

With every chunk having access to the environmental noise maps and its neighboring chunks, the generation of biomes, vegetation, bodies of water and other content can build on that. Regarding our very next step, which is the mapping of biomes, our procedure for implementing them consists of two phases (Issues #4 and #5) and looks as follows:

- [Issue #4](https://github.com/ZeAntonioM/WGen-2D/issues/4): We introduce different types of biomes, each having a unique ruleset and lookup table. In this step, the raw noise data propagated to each chunk serves as the basis of decision for the placement of biomes.

- [Issue #5](https://github.com/ZeAntonioM/WGen-2D/issues/5): Due to the usage of hard rules, the transition will mirror this trend and be abrupt at first. The next step therefore is to blend different biomes that are located next to each other. It is critical in this step, that the neighbors of the currently generated chunk can be queried and taken into account, to ensure smooth biome blending at chunk borders.

- [Issue #6](https://github.com/ZeAntonioM/WGen-2D/issues/6) and [Issue #7](https://github.com/ZeAntonioM/WGen-2D/issues/7): Similarly, but not planned out in detail and fed as issues in small steps into our repository yet, is the placement of the remaining content of the world, in particular the water system (which mainly uses a threshold on an altitude map) and the vegetation, rocks and settlements (which are scattered based on probability distributions). 
