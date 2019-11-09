import neat
import board
import os

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    b = board.Board(500, 500)
    top = p.run(b.sim_one_gen, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(top))

def render(self, screen):
    for creature in self.creatures:
        creature.render(screen)
    for food in self.food:
        food.render(screen)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'species_config.txt')
    run(config_path)
