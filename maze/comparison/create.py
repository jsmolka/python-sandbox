import benchmark as bm
from maze import Maze


def pmaze(rows, cols):
    """Create maze with recursive backtracking."""
    m = Maze()
    m.create(rows, cols, Maze.Create.BACKTRACKING)


def cmaze(rows, cols):
    """Create maze with recursive backtracking in C."""
    m = Maze()
    m.create(rows, cols, Maze.Create.C)


size = (100, 100)
bm.versus(pmaze, cmaze, 10, size)
input()
