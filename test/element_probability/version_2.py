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

pool = list()
pool.append(0)
for i in range(1, len(l) + 1):  # Create pool with probabilities
    pool.append(pool[i - 1] + l[i - 1].prob / maxprob)

for i in range(0, len(pool)):
    if pool[i] <= r <= pool[i + 1]:
        print("Currentprob:", pool[i + 1])
        print("Element value:", l[i + 1].value)
        print("Element probability:", l[i + 1].prob)
        break

sw.stop()
sw.print_elapsed_time()

input()
