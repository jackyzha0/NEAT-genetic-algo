# Poster

## Goal

The poster for our project will look to explain both our implementation of NEAT and the mathematics behind it in a less technical way. The casual reader should be able to understand the core concepts of genetic algorithms through the poster.

## Approach

Our group has already done some preliminary research into genetic algorithms and identified the main sections for our poster. We've discovered that all genetic algorithms employ the same rough outline:

1. Start the simulation
2. Initialize the population
3. Compute the original fitness score
4. While the population has not reached our desired number of generations...
    1. First, select the fittest parents to reproduce
    2. Then, a "crossover point" is chosen at random. This is the cutoff showing where parent A's DNA will be used versus parent B's.
    3. Finally, the genes will be mutated with a low random probability.
    4. (Compute the new fitness)
5. Stop the simulation once enough iterations have completed

From here, we will go into more depth about what the algorithm entails.

