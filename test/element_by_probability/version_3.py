import random
from stopwatch import *


class RandomClass:
    value = None
    prob = None

    def __init__(self, value):
        """Constructor"""
        self.value = value
        self.prob = random.random()


r = random.random()
print("R:", r)

l = list()
for i in range(0, 100000):  # Create list
    l.append(RandomClass(i))

sw = Stopwatch()
sw.start()

maxprob = 0
for elem in l:  # Calculate maxprob
    maxprob += elem.prob
print("Maxprob:", maxprob)

currentprob = 0
for elem in l:  # Go through elements
    currentprob += elem.prob / maxprob
    if r <= currentprob:
        print("Currentprob:", currentprob)
        print("Element value:", elem.value)
        print("Element probability:", elem.prob)
        break

sw.stop()
sw.print_elapsed_time()

input()
