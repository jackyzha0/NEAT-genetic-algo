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
        '''
        Bounce creature off the wall and reflect its angle in the boundary
        given width and height of screen
        '''
        if self.x > (width - self.size):
            self.x = 2 * (width - self.size) - self.x
            self.angle = - self.angle
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle

        if self.y > (height - self.size):
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle


    def accel(self, a):
        self.velocity += a

    def turn(self, r):
        self.angle += r


    def collide(self, loc):
        '''
        Check if the particle collides with any other particles in the given
        list of creatures

        Return: list of collided creature indexes
        '''
        collision_indexes = []
        for i2, c2 in enumerate(loc):
            dx = self.x - c2.x
            dy = self.y - c2.y

            distance = math.hypot(dx, dy) # distance between two creatures
            combined_radius = self.size + c2.size

            if distance < combined_radius:
                collision_indexes.append(i2) # add collided creature's index to list

        return collision_indexes
