import neat
import board
import os
import pygame

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

    # setup pygame
    WIDTH = 500
    HEIGHT = 500

    NUMBER_0F_GEN = 100

    # Run for up to 50 generations.
    b = board.Board(WIDTH, HEIGHT)

    top = p.run(b.sim_one_gen, NUMBER_0F_GEN)

    # show final stats
    print('\nBest genome:\n{!s}'.format(top))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'species_config.txt')
    run(config_path)
