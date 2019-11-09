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
    WIDTH = 1000
    HEIGHT = 1000
    BACKGROUND_COLOR = (255,255,255) # white
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('NATURAL SELECTION SIMULATION')
    screen.fill(BACKGROUND_COLOR)

    # Run for up to 50 generations.
    b = board.Board(WIDTH, HEIGHT, screen)

    top = p.run(b.sim_one_gen, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(top))

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'species_config.txt')
    run(config_path)
