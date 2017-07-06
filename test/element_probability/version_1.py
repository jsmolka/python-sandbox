import random
from stopwatch import *


class RandomClass:
    value = None
    prob = None

    def __init__(self, value):
        """Constructor"""
        self.value = value
        self.prob = random.random()


sw = Stopwatch()
sw.start()

l = list()
for i in range(0, 100000):  # Create list
    l.append(RandomClass(i))

pool = list()
for elem in l:  # Create pool
    i = int(elem.prob * 100)
    for j in range(0, i):
        pool.append(elem)

r = random.randint(0, len(pool))  # Pick random element
elem = pool[r]

sw.stop()

print("Pool length:", len(pool))
print("R:", r)
print("Element value:", elem.value)
print("Element probability:", elem.prob)
sw.print_elapsed_time()

input()
