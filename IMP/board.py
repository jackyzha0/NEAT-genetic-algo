# Class definition for game board
import creatures
import food
import random
import math
import neat

class Board():
    def __init__(self, w, h, foodspawn = 0.1):
        self.width = w  # dimensions of board
        self.height = h
        self.foodspawnthresh = 1 - foodspawn
        self.generation = 0  # current generation
        self.food = []  # initialized later
        self.creatures = []  # initialized later
        self.GEN_TIMEOUT = 1800
        self.FOOD_GEN_DELTA = 5

    def board_tick(self):
        # food generation
        for f in self.food:
            # spawn if random exceeds threshold
            if random.random() > self.foodspawnthresh:
                # new x,y position with +/- 5 delta from current food position
                x, y = f.x + random.randint(-self.FOOD_GEN_DELTA, self.FOOD_GEN_DELTA), f.y + random.randint(-self.FOOD_GEN_DELTA, self.FOOD_GEN_DELTA)

                # if in range, add new food to foodlist
                if x > 0 and x < self.width and y > 0 and y < self.height:
                    self.food.append(food.Food(x, y, size=random.random() * 3))

        for i, c in enumerate(self.creatures):
            for i2 in c.collide(self.creatures[i+1:]):
                c2 = self.creatures[i2]       # get creature from list using index

                if c.size > c2.size:          # check which creature is bigger
                    self.creatures.pop(i2)    # kill the smaller one
                    c.energy += c2.size       # increase the bigger one's energy by the smaller one's size
                else:
                    self.creatures.pop(i)
                    c2.energy += c.size


    def closest(self, x, y, size):
        prey_min_r = math.inf  # closest distance doesnt exist, assume infinity
        prey_min_theta = 0  # angle shouldnt matter when dist is infinity
        predator_min_r = math.inf
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
        self.food = []
        # create two pieces of food for every creature
        for _ in range(len(genomes)*2):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.random()*3
            f = food.Food(x, y, size)
            self.food.append(f)

        nets = []
        g_l = []
        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            self.creatures.append(creatures.Creature(x=random.randint(0, self.width), y=random.randint(0, self.height), size=random.randint(1,10)))
            g_l.append(genome)

        while self.creatures and self.ticks_total < self.GEN_TIMEOUT:
            self.board_tick()
            for i, creature in enumerate(self.creatures):
                g_l[i].fitness += 1
                creature.tick()

                if creature.dead:
                    # !!! pop g_l, nets, creatures
                    pass
                else:
                    closest = self.closest(creature.x, creature.y, creature.size)

                    net_out = nets[self.creatures.index(creature)].activate(closest)

                    creature.accel(net_out[0])
                    creature.turn(net_out[1] * math.pi)

    def render(self, screen):
        for creature in self.creatures:
            creature.render(screen)
        for food in self.food:
            food.render(screen)

def find_r_theta(x1, y1, x2, y2):
    theta = math.tan((x2 - x1) / (y2 - y1 + 1e-8))
    r = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return r, theta
