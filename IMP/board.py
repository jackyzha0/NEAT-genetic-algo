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
        self.GEN_TIMEOUT = 1800  # Constant for generation timeout
        self.FOOD_GEN_DELTA = 5  # Constant for food generation position change

    def board_tick(self):
        '''
        Updates board every tick by spawning new food and checking for collisions.
        '''
        for f in self.food:
            # spawn if random exceeds threshold
            if random.random() > self.foodspawnthresh:

                # new x,y position with +/- FOOD_GEN_DELTA constant from current food position
                nx = f.x + random.randint(-self.FOOD_GEN_DELTA, self.FOOD_GEN_DELTA)
                ny = f.y + random.randint(-self.FOOD_GEN_DELTA, self.FOOD_GEN_DELTA)
                x, y = nx, ny

                # if in range, add new food to foodlist
                if x > 0 and x < self.width and y > 0 and y < self.height:
                    self.food.append(food.Food(x, y, size=random.random() * 3))  # random size

        for i, c in enumerate(self.creatures):
            for i2 in c.collide(self.creatures[i+1:]):
                c2 = self.creatures[i2]       # get creature from list using index

                if c.size > c2.size:          # check which creature is bigger
                    self.creatures.pop(i2)    # kill the smaller one
                    c.energy += c2.size       # increase the bigger one's energy by the smaller one's size
                else:
                    self.creatures.pop(i)
                    c2.energy += c.size


    def closest(self, x: int, y: int, size: int) -> [int, float, int, float]:
        '''
        Find closest predator and prey to x,y, given size.
        Predator is any food/creature that is of strictly greater size
        Prey is any food/creature that is strictly smaller
        '''
        prey_min_r = math.inf  # closest distance doesnt exist, assume infinity
        prey_min_theta = 0  # angle shouldnt matter when dist is infinity
        predator_min_r = math.inf
        predator_min_theta = 0

        for c in self.food and self.creatures:  # iterate through all creatures and food
            r, theta = find_r_theta(x, y, c.x, c.y)  # calculate distance and angle to object
            if c.size > size: # check predator
                if r < predator_min_r:
                    predator_min_r = r
                    predator_min_theta = theta
            else: # is prey
                if r < prey_min_r:
                    prey_min_r = r
                    prey_min_theta = theta

        return [prey_min_r, prey_min_theta, predator_min_r, predator_min_theta]

    def sim_one_gen(self, genomes: [(int, neat.genome.DefaultGenome)], config: neat.config.Config):
        '''
        Simulate one generation of creatures. Each generation is capped at GEN_TIMEOUT ticks.
        '''
        self.generation += 1  # increment generation

        self.ticks_total = 0  # reset current ticks

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

        # init list of neural networks and genomes
        nets = []
        g_l = []

        # iterate genomes
        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)  # from python-neat
            nets.append(net)
            c = creatures.Creature(x=random.randint(0, self.width), y=random.randint(0,  self.height), size=random.randint(1, 10))  # create creature
            self.creatures.append(c)
            g_l.append(genome) # append genome to genome list

        # simulate!
        while self.creatures and self.ticks_total < self.GEN_TIMEOUT:
            self.board_tick()  # update board
            for i, creature in enumerate(self.creatures):  # update all creatures
                g_l[i].fitness += 1  # increment fitness by 1 for every tick that its alive
                creature.tick()  # tick creature

                if creature.dead:
                    # !!! pop g_l, nets, creatures
                    pass
                else:
                    closest = self.closest(creature.x, creature.y, creature.size)

                    # get neural network output given input of closest
                    net_out = nets[self.creatures.index(creature)].activate(closest)

                    # modify creature accel based on nn output
                    creature.accel(net_out[0])

                    # modify creature direction based on nn output
                    creature.turn(net_out[1] * math.pi)

    def render(self, screen):
        '''
        Small function to blit all creatures and food onto
        PyGame Display
        '''
        for creature in self.creatures:
            creature.render(screen)
        for food in self.food:
            food.render(screen)

def find_r_theta(x1: int, y1: int, x2: int, y2: int) -> (float, float):
    '''
    Small helper function to calculate distance and angle between
    two points (x1,y2) and (x2,y2)
    Theta is calculated relative to the top (0 radians) and the bottom (-pi/pi)
    '''
    theta = math.tan((x2 - x1) / (y2 - y1 + 1e-8))  # add small epsilon to prevent divide by zero
    r = math.hypot((x2-x1), (y2-y1))
    return r, theta
