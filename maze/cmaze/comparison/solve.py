from benchmark import *
from maze import *


def pmaze(args):
    m = Maze()
    m.maze = args
    m.solve(0, 0, Algorithm.Solve.DEPTH)


def cmaze(args):
    m = CMaze()
    m.maze = args
    m.solve(0, 0)


t = CMaze()
t.create(100, 100)
t = t.maze
compare(pmaze, cmaze, t, t, 10)
input()
