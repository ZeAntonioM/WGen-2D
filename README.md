<div align="center">
<b><font size="6">Procedural Generation of a Coherent Infinite 2D Landscape</font></b>
<br>
<font size="3">(Final Report)</font>
<br>
José Martins, Francisco Cardoso, Cedric Hartz
</div>

## Abstract

This project explores procedural content generation of an infinite 2D top-down world using a chunk-based approach. The generated world is composed of different biomes, derived from multiple environmental maps (i.e., altitude, temperature, precipitation), focusing on local and regional consistency and coherency. The goal is to study how noise-based algorithms mixed with rule-based decisions can produce large-scale worlds with smooth biome transitions and context-aware content placement.

## Introduction

Many videogames are centered around a large world, in which players can fight, accomplish quests, explore and maybe build their own structures. Game developers therefore face the need to create such a large map for the game to take place. This is not an easy task, especially for small studios and teams, and consumes time and money. This is why the demand for PTG (procedural terrain generation) is ever increasing.

The main challenge for PTG is to create a coherent and structured world, that does not look purely random. While different games adopt different approaches, they often share the same underlying goal: ensuring that the generated world makes sense according to its own internal rules.

Looking at Minecraft as a well known example for PTG, its infinite world is composed of biomes that transition in a consistent and recognizable way, while RimWorld divides its world into multiple regions that may repeat biomes or patterns. These worlds do not necessarily follow real-world planetary rules, but they maintain internal consistency that makes them believable and playable.

Observing how such games balance repetition, large-scale structure, and local detail motivated us to explore similar ideas. This project focuses on understanding how coherence can be preserved in an infinite world, valuing coherence over realism. To preserve flexibility and usability of the generation, we plan to make use of relatively simple mechanisms such as continuous noise fields, simple physics-based approaches and rule- and probability-based decisions. The constraint of generating an infinite world requires a real-time performant generation and forces us to implement simulations and decisions relying only on local data, instead of a full global simulation.

## Related Work

[Todo:
- literature
- introduce our main source (AutoBiomes) and explain how we can use the presented methods for our project, but still have to modify them to be infinitely scalable

]

## Methodology of our approach

[Todo: 
- explanation and justication for the methodology chosen
- possibly failed attempts, evolution of our approach

]

## Experiments and Results

[Todo:
- (we still have to do the experiments)
- describe what we did
- what are the results?
- how are they useful, how can they be applied in different contexts, in the real world, by other people?

]

## How to run our generator

[Todo:
- how to run the code
- what do you have to know about the generator

]

## Conclusion

[Todo:
- overview of our results
- what is different from our initial plan

]

### Future work

[Todo]

## Appendix

[Todo:
- images, diagrams, useful information

]