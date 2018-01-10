import cursor
from constants import *


def render(grid):
    i = 0  # TODO: remove counter
    while True:
        cursor.reset()
        string = ""
        for x in range(0, grid.rows):
            for y in range(0, grid.cols):
                string += TYPES[grid[x, y]]
            string += "\n"
        print(string, end="")
        i += 1
        print("frame:", i)