import benchmark as bm
from maze import Maze


def pmaze(array):
    """Solves maze with depth-first search."""
    m = Maze()
    m.maze = array
    m.solve((), (), Maze.Solve.DEPTH)


def cmaze(array):
    """Solves maze with depth-first search in C."""
    m = Maze()
    m.maze = array
    m.solve((), (), Maze.Solve.C)


mz = Maze()
mz.create(100, 100, Maze.Create.C)
bm.versus(pmaze, cmaze, 50, mz.maze)
input()
