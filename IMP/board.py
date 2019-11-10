# Class definition for game board
import creatures
import food
import random
import math
import pygame
import neat
import sys

class Board():
    def __init__(self, w, h, foodspawn = 0.1):
        self.width = w  # dimensions of board
        self.height = h
        self.foodspawnthresh = 1 - foodspawn
        self.generation = 0  # current generation
        self.food = []  # initialized later
        self.creatures = []  # initialized later
        self.GEN_TIMEOUT = 12000  # Constant for generation timeout
        self.FOOD_GEN_DELTA = 5  # Constant for food generation position change
        self.MAX_FOOD = 500

        pygame.init()
        self.BACKGROUND_COLOR = (220,220,220) # white
        pygame.display.set_caption('NATURAL SELECTION SIMULATION')
        self.screen = pygame.display.set_mode((w, h))
        self.screen.fill(self.BACKGROUND_COLOR)

    def board_tick(self):
        '''
        Updates board every tick by spawning new food and checking for collisions.
        '''
        # check food amount
        if len(self.food) < self.MAX_FOOD:
            for f in self.food:
                # spawn if random exceeds threshold
                if random.random() > self.foodspawnthresh:

                    # new x,y position with +/- FOOD_GEN_DELTA constant from current food position
                    nx = f.x + random.randint(-self.FOOD_GEN_DELTA, self.FOOD_GEN_DELTA)
                    ny = f.y + random.randint(-self.FOOD_GEN_DELTA, self.FOOD_GEN_DELTA)
                    x, y = nx, ny

                    # if in range, add new food to foodlist
                    if x > 0 and x < self.width and y > 0 and y < self.height:
                        self.food.append(food.Food(x, y, size=random.randint(2, 5)))  # random size

        for i, c in enumerate(self.creatures):
            for col_creat in c.collide(self.creatures[i+1:]):
                if c.size > col_creat.size:          # check which creature is bigger
                    self.creatures.remove(col_creat)    # kill the smaller one
                    c.energy += col_creat.size * 5       # increase the bigger one's energy by the smaller one's size
                else:
                    self.creatures.pop(i)
                    col_creat.energy += c.size
            for f in c.collide(self.food):
                if c.size > f.size:          # check if can eat
                    self.food.remove(f)
                    c.energy += f.size
                    self.g_l[i].fitness += f.size * 5

        if self.ticks_total % 2 == 0:
            self.render()

        self.ticks_total += 1

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

        for c in self.food + self.creatures:  # iterate through all creatures and food
            r, theta = find_r_theta(x, y, c.x, c.y, self.height)  # calculate distance and angle to object
            if c.size > size: # check predator
                if r < predator_min_r:
                    predator_min_r = r
                    predator_min_theta = theta
            if c.size < size: # is prey
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
        for _ in range(self.MAX_FOOD):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.random()*3
            f = food.Food(x, y, size)
            self.food.append(f)

        # init list of neural networks and genomes
        nets = []
        self.g_l = []

        # iterate genomes
        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)  # from python-neat
            nets.append(net)
            c = creatures.Creature(x=random.randint(0, self.width), y=random.randint(0,  self.height), size=random.randint(5, 10))  # create creature
            self.creatures.append(c)
            self.g_l.append(genome) # append genome to genome list

        # simulate!
        while self.creatures and (self.ticks_total < self.GEN_TIMEOUT):
            self.board_tick()  # update board
            for i, creature in enumerate(self.creatures):  # update all creatures
                creature.tick()  # tick creature
                creature.bounce(self.width, self.height)

                if creature.dead:
                    c_i = self.creatures.index(creature)  # index of current creatures
                    self.g_l.pop(c_i)
                    self.creatures.pop(c_i)
                    nets.pop(c_i)
                else:
                    closest = self.closest(creature.x, creature.y, creature.size)

                    # get neural network output given input of closest
                    net_out = nets[self.creatures.index(creature)].activate(closest)

                    # modify creature accel based on nn output
                    creature.accel(net_out[0])

                    # modify creature direction based on nn output
                    creature.turn(net_out[1] * math.pi)

    def render(self):
        '''
        Small function to blit all creatures and food onto
        PyGame Display
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.screen.fill(self.BACKGROUND_COLOR)

        for creature in self.creatures:
            creature.render(self.screen)
        for food in self.food:
            food.render(self.screen)

        pygame.display.flip()

def find_r_theta(x1: int, y1: int, x2: int, y2: int, normfact: int) -> (float, float):
    '''
    Small helper function to calculate distance and angle between
    two points (x1,y2) and (x2,y2)
    Theta is calculated relative to the top (0 radians) and the bottom (-pi/pi)
    '''
    theta = math.atan((x2 - x1) / (y2 - y1 + 1e-8))  # add small epsilon to prevent divide by zero
    r = math.hypot((x2-x1), (y2-y1)) / normfact
    return r, theta
