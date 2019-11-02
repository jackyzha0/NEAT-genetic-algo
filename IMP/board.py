# Class definition for game board
import creatures
import food
import random
import pygame

class Board():
    def __init__(self, w, h, foodspawn = 0.1, initpop = 50, initfood = 100):
        self.width = w
        self.height = h
        self.foodspawnchance = foodspawn
        self.generation = 0
        self.ticks_total = 0

        # init creatures
        self.creatures = [creatures.Creature(x=random.randint(0, w), y=random.randint(0, h), size=20) for _ in range(initpop)]

        # init food
        self.food = [food.Food(x=random.randint(0, w), y=random.randint(0, h), size=3) for _ in range(initfood)]

    def tick(self):
        self.creatures = [c.tick() for c in creatures]
        self.ticks_total += 1

        # iterate through each food item and try spawn

    def render(self, screen):
        for creature in self.creatures:
            creature.render(screen)
        for food in self.food:
            food.render(screen)
