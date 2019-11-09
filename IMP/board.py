# Class definition for game board
import creatures
import food
import random
import math
import neat

class Board():
    def __init__(self, w, h, foodspawn = 0.1):
        self.width = w
        self.height = h
        self.foodspawnthresh = 1 - foodspawn
        self.generation = 0
        self.food = [] # initialized later
        self.creatures = [] # initialized later

    def board_tick(self):
        # iterate through each food item and spawn with prob
        for f in self.food:
            if random.random() > self.foodspawnthresh:
                x, y = f.x + self.random.randint() * 10, f.y + self.random.randint() * 10
                if x > 0 and x < self.width and y > 0 and y < self.height:
                    self.food.append(food.Food(x, y, val=random.random(0, 3)))

        # !!! check for collisions

    def closest(self, x, y, size):
        prey_min_r = 1e10
        prey_min_theta = 0
        predator_min_r = 1e10
        predator_min_theta = 0

        for c in self.food and self.creatures:
            r, theta = find_r_theta(x, y, c.x, c.y)
            if c.size > size:
                if r < predator_min_r:
                    predator_min_r = r
                    predator_min_theta = theta
            else:
                if r < prey_min_r:
                    prey_min_r = r
                    prey_min_theta = theta

        return [prey_min_r, prey_min_theta, predator_min_r, predator_min_theta]

    def sim_one_gen(self, genomes, config):
        self.generation += 1

        self.ticks_total = 0

        # init creatures
        self.creatures = []

        # init food
        self.food = [food.Food(x=random.randint(0, self.width), y=random.randint(0, self.height), val=random.random()*3) for _ in range(len(genomes) * 2)] # create two pieces of food for every creature

        nets = []
        g_l = []
        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            self.creatures.append(creatures.Creature(x=random.randint(0, self.width), y=random.randint(0, self.height)))
            g_l.append(genome)

        while self.creatures and self.ticks_total < 1800:
            self.board_tick()
            for i, creature in enumerate(self.creatures):
                g_l[i].fitness += 1
                creature.tick()

                if creature.dead:
                    # !!! pop g_l, nets, creatures
                    pass
                else:
                    preyr, preyt, predr, predt = self.closest(creature.x, creature.y, creature.size)

                    net_out = nets[creatures.index(creature)].activate(preyr, preyt, predr, predt)

                    creature.accel(net_out[0])
                    creature.turn(net_out[1] * math.pi)

    def render(self, screen):
        for creature in self.creatures:
            creature.render(screen)
        for food in self.food:
            food.render(screen)

def find_r_theta(x1, y1, x2, y2):
    theta = math.tan((x2 - x1) / (y2 - y1 + 1e-8))
    r = math.sqrt((x2-x1)**2 - (y2-y1)**2)
    return r, theta
