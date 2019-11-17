# Class definition for food
import random

import pygame


class Food():
    def __init__(self, x, y, size):
        '''
        Basic Food class
        '''
        self.x = x
        self.y = y
        self.colour = (255, 0, 0)
        self.size = size  # determines what kind of creatures can eat it
        # and how much energy it gives

    def render(self, screen):
        '''
        Blit self onto PyGame surface
        '''
        pygame.draw.circle(screen, self.colour, (int(
            self.x), int(self.y)), int(self.size), 0)
