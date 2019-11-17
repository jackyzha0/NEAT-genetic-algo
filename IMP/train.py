import neat
import board
import os
import pygame
import matplotlib.pyplot as plt
import visualize


def run(config_file):
    # read config from species_config.txt
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # initialize population
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    # setup pygame
    WIDTH = 500
    HEIGHT = 500

    NUMBER_0F_GEN = 100

    # Run for up to 50 generations.
    b = board.Board(WIDTH, HEIGHT)

    top = p.run(b.sim_one_gen, NUMBER_0F_GEN)

    # x axis values
    gens = list(range(1, NUMBER_0F_GEN + 1))
    # y axis values
    avg_fitness = stats.get_fitness_mean()
    best_fitness = stats.get_fitness_stat(customize_max)

    plt.plot(gens, avg_fitness)
    plt.plot(gens, best_fitness)

    plt.xlabel('Generations')

    # giving a title to my graph
    plt.title('Generations vs. Fitness Score')

    # function to show the plot
    plt.show()

    # show final stats
    print('\nBest genome:\n{!s}'.format(top))

    visualize.draw_net(config, top, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


def customize_max(values):
    values = list(values)
    return max(values)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'species_config.txt')
    run(config_path)
