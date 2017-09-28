from benchmark import *
from maze import *


def pmaze(args):
    m = Maze()
    m.create(args[0], args[1], Algorithm.Create.BACKTRACKING)


def cmaze(args):
    m = Maze()
    m.create(args[0], args[1], Algorithm.Create.C)


size = (100, 100)
compare(pmaze, cmaze, size, size, 10)
input()
