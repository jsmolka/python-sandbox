import random
from benchmark import *


class RandomClass:
    value = None
    prob = None

    def __init__(self, value):
        """Constructor"""
        self.value = value
        self.prob = random.random()


def v1(l):
    pool = list()
    for e in l:  # Create pool
        len_ = int(e.prob * 100)
        for j in range(0, len_):
            pool.append(e)

    r = random.randint(0, len(pool))  # Pick random element
    return pool[r]


def v2(l):
    r = random.random()
    max_prob = 0
    for e in l:  # Calculate max prob
        max_prob += e.prob

    pool = list()
    pool.append(0)
    for i in range(1, len(l) + 1):  # Create pool with probabilities
        pool.append(pool[i - 1] + l[i - 1].prob / max_prob)

    for i in range(0, len(pool)):
        if pool[i] <= r <= pool[i + 1]:
            return pool[i + 1]


def v3(l):
    r = random.random()
    max_prob = 0
    for e in l:  # Calculate max prob
        max_prob += e.prob

    current_prob = 0
    for e in l:  # Go through elements
        current_prob += e.prob / max_prob
        if r <= current_prob:
            return e


rl = list()
for i in range(0, 10000):  # Create list
    rl.append(RandomClass(i))


benchmark(v1, rl, 10)
benchmark(v2, rl, 10)
benchmark(v3, rl, 10)
input()
