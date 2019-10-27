# Class definition for creatures
import math

class Creature():
    def __init__(self, x, y, genomeLength = 10):
        self.x = x
        self.y = y
        self.genome = self.genGenome(genomeLength)
        # fitness
        # facing
        # vel
        # size

    def genGenome(self, length):
        res = []
        for x in range(length):
            res.append(chr(random.randint(0, 97)))
            
    def tick(self):
        # update properties using facing and vel
        pass
