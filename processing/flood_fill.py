import numpy as np
from pyprocessing import *
from random import randint

# Configuration
length = 100
scale = 8
origins = 2

# Define variables
m = np.zeros((length, length), dtype=np.bool_)
cells = []
frontier = []
for i in range(0, origins):
    x, y = randint(0, length - 1), randint(0, length - 1)
    cells.append((x, y))
    frontier.append((x, y))
    m[x, y] = True

dir_one = [
    lambda x, y: (x + 1, y),
    lambda x, y: (x - 1, y),
    lambda x, y: (x, y - 1),
    lambda x, y: (x, y + 1)
]


def out_of_bounds(x, y, length):
    return True if x < 0 or y < 0 or x >= length or y >= length else False


def flood(frontier):
    global m, cells, dir_one
    cells = [cell for cell in frontier]
    new_frontier = []
    while frontier:
        x, y = frontier.pop()
        for direction in dir_one:
            tx, ty = direction(x, y)
            if not out_of_bounds(tx, ty, length) and not m[tx, ty]:
                new_frontier.append((tx, ty))
                m[tx, ty] = True
    if not new_frontier:
        noLoop()
    return new_frontier


def draw_cells():
    global cells, scale
    fill(randint(128, 255))
    for x, y in cells:
        rect(y * scale, x * scale, scale, scale)
    cells = []


def setup():
    global length, scale
    size(length * scale, length * scale)
    background(0)
    noStroke()
    colorMode(HSB)
    draw_cells()


def draw():
    global frontier
    frontier = flood(frontier)
    draw_cells()


run()
