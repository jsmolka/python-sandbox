from benchmark import *
from maze import *


def pmaze(args):
    m = Maze()
    m.maze = args
    m.solve(0, 0, Maze.Solve.DEPTH)


def cmaze(args):
    m = Maze()
    m.maze = args
    m.solve(0, 0, Maze.Solve.C)


t = Maze()
t.create(100, 100, Maze.Create.C)
t = t.maze
compare(pmaze, cmaze, t, t, 10)
input()
