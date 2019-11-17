import neat
import board
import os
import pygame
import matplotlib.pyplot as plt
import visualize


def run(config_file, useSaved = True, rest_gen = 99):
    # read config from species_config.txt
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    # setup pygame
    WIDTH = 500
    HEIGHT = 500

    # Run for up to 50 generations.
    b = board.Board(WIDTH, HEIGHT)
    if useSaved:
        s = 'neat-checkpoint-{g}'.format(g = rest_gen)
        p = neat.Checkpointer.restore_checkpoint(s)
        p.run(b.sim_one_gen, 3)
    else:
        NUMBER_0F_GEN = 100
        # initialize population
        p = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(10))

        top = p.run(b.sim_one_gen, NUMBER_0F_GEN)

        # show final stats
        print('\nBest genome:\n{!s}'.format(top))

        visualize.plot_stats(stats, ylog=False, view=True)
        visualize.plot_species(stats, view=True)
        visualize.draw_net(config, top, True)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'species_config.txt')
    run(config_path)
