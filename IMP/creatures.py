# Class definition for creatures
import math

class Creature():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.energy = 100. # starting energy, dies if energy = 0
        self.facing = 0 # [-pi, pi]
        self.vel = 0
        self.dead = False

    def tick(self):
        # consume energy, check if dead
        self.energy -= self.vel + (0.1 * self.size)
        if self.energy <= 0:
            self.dead = True

        # update x,y based on vel and facing
        dx = math.sin(self.facing) * self.vel
        dy = math.cos(self.facing) * self.vel
        x += dx
        y += dy

    def accel(self, a):
        self.vel += a

    def turn(self, r):
        self.facing += r
