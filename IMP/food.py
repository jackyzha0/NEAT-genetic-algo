# Class definition for food

import pygame

class Food():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.colour = (255, 0, 102)
        self.size = size

    def render(self, screen):
        pygame.draw.circle(screen, self.colour,
        (self.x, self.y), self.size, 0)
