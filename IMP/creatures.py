# Class definition for creatures
import math
import pygame
import random


class Creature():
    def __init__(self, x: int, y: int, size: int):
        '''
        Basic Creature class
        '''
        self.x = x
        self.y = y
        self.size = size  # determines what it can eat, also affects energy consumption
        self.colour = (random.randrange(
            254), random.randrange(254), random.randrange(254))
        self.energy = 500.  # starting energy, dies if energy = 0
        self.angle = (random.random() * 2 * math.pi) - math.pi  # [-pi, pi]
        self.velocity = 0
        self.dead = False
        self.SIZE_ENERGY_RATIO = 0.125  # energy penalty for movement based on size
        self.VEL_MAX = 5

    def tick(self):
        '''
        Update self properties
        '''
        # consume energy, check if dead
        self.energy -= abs(self.velocity) + \
            (self.SIZE_ENERGY_RATIO * self.size)
        if self.energy <= 0:
            self.dead = True
            self.energy = 0

        # update x,y based on vel and angle
        dx = math.sin(self.angle) * self.velocity
        dy = math.cos(self.angle) * self.velocity
        self.x += dx
        self.y += dy

    def render(self, screen, debug):
        '''
        Blit self onto PyGame surface
        '''
        # print(self.x, self.y, self.energy)
        pygame.draw.circle(screen, self.colour, (int(
            self.x), int(self.y)), int(self.size), 0)

        # if debug:
        x2 = int(math.sin(self.angle) * self.velocity * 5) + int(self.x)
        y2 = int(math.cos(self.angle) * self.velocity * 5) + int(self.y)
        pygame.draw.line(screen, (0, min((self.energy/500), 1)
                                  * 255, 0), (int(self.x), int(self.y)), (x2, y2), 2)

    def accel(self, a: float):
        '''
        Change velocity by a.
        Called by board
        '''
        if abs(self.velocity) < self.VEL_MAX:
            self.velocity += a

    def turn(self, r: float):
        '''
        Changle angle by r
        Called by board
        '''
        self.angle = r

    def collide(self, loc):
        '''
        Check if the particle collides with any other creature in the given
        list of creatures

        Return: list of collided creatures
        '''
        collisions = []
        for c2 in loc:
            dx = self.x - c2.x
            dy = self.y - c2.y

            distance = math.hypot(dx, dy)  # distance between two creatures
            combined_radius = self.size + c2.size

            if distance < combined_radius:
                collisions.append(c2)  # add collided creature's index to list

        return collisions
