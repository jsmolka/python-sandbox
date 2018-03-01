import benchmark as bm
import random


class RandomClass:
    """Random class."""
    def __init__(self, value):
        """Constructor."""
        self.value = value
        self.prob = random.random()


@bm.benchmark(100)
def version1(lst):
    """Version 1."""
    pool = list()
    for x in lst:  # Create pool
        for j in range(int(x.prob * 100)):
            pool.append(x)
    idx = random.randint(0, len(pool))  # Pick random element
    return pool[idx]


@bm.benchmark(100)
def version2(lst):
    """Version 2."""
    rand = random.random()
    total = 0
    for x in lst:  # Calculate max prob
        total += x.prob

    pool = []
    pool.append(0)
    for idx in range(1, len(lst) + 1):  # Create pool with probabilities
        pool.append(pool[idx - 1] + lst[idx - 1].prob / total)

    for idx in range(len(pool)):
        if pool[idx] <= rand <= pool[idx + 1]:
            return pool[idx + 1]


@bm.benchmark(100)
def version3(lst):
    """Version 3"""
    rand = random.random()
    total = 0
    for x in lst:  # Calculate max prob
        total += x.prob

    current = 0
    for x in lst:  # Go through elements
        current += x.prob / total
        if rand <= current:
            return x


if __name__ == "__main__":
    rand_lst = [RandomClass(idx) for idx in range(10000)]

    version1(rand_lst)
    version2(rand_lst)
    version3(rand_lst)
    input()
