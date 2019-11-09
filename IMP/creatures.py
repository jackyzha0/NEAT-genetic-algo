# Class definition for creatures
import math
import pygame
from random import randrange

class Creature():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.energy = 100. # starting energy, dies if energy = 0
        self.angle = 0 # [-pi, pi]
        self.velocity = 0
        self.dead = False

    def tick(self):
        # consume energy, check if dead
        self.energy -= self.velocity + (0.1 * self.size)
        if self.energy <= 0:
            self.dead = True

        # update x,y based on vel and angle
        dx = math.sin(self.angle) * self.velocity
        dy = math.cos(self.angle) * self.velocity
        self.x += dx
        self.y += dy

    def render(self, screen):
        colour = (randrange(254), randrange(254), randrange(254))
        #outline
        pygame.draw.circle(screen, colour,
        (self.x, self.y), self.size, 2)
        #solid
        pygame.draw.circle(screen, colour,
        (self.x, self.y), self.size - 5, 0)


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


    def accel(self, a):
        self.velocity += a

    def turn(self, r):
        self.angle += r
