from benchmark import *


def enumerate_(l):
    for i, e in enumerate(l):
        pass


def range_(l):
    for i in range(0, len(l)):
        pass


tl = [i for i in range(0, 100000)]

compare(enumerate_, range_, tl, tl, 100)
input()
