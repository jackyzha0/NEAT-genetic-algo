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
        self.colour = (random.randrange(254), random.randrange(254), random.randrange(254))
        self.energy = 100.  # starting energy, dies if energy = 0
        self.angle = 0  # [-pi, pi]
        self.velocity = 0
        self.dead = False
        self.SIZE_ENERGY_RATIO = 0.1  # energy penalty for movement based on size

    def tick(self):
        '''
        Update self properties
        '''
        # consume energy, check if dead
        self.energy -= self.velocity + (self.SIZE_ENERGY_RATIO * self.size)
        if self.energy <= 0:
            self.dead = True

        # update x,y based on vel and angle
        dx = math.sin(self.angle) * self.velocity
        dy = math.cos(self.angle) * self.velocity
        self.x += dx
        self.y += dy

    def render(self, screen):
        '''
        Blit self onto PyGame surface
        '''

        # outline
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, 2)
        
        # solid
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size - 5, 0)


    def bounce(self, width, height):
        if self.x > (width - self.size):
            self.x = 2 * (width - self.size) - self.x
            self.angle = - self.angle
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle


    def accel(self, a: float):
        '''
        Change velocity by a.
        Called by board
        '''
        self.velocity += a

    def turn(self, r: float):
        '''
        Changle angle by r
        Called by board
        '''
        self.angle += r
