import numpy as np
from pyprocessing import *
from opensimplex import *

# Configuration
WIDTH = 1100
HEIGHT = 900
SCALE = 25
ROWS = round(HEIGHT / SCALE)
COLS = round(WIDTH / SCALE)
terrain = np.zeros((COLS, ROWS))
simplex = OpenSimplex()
FLYING = 0
FLYING_STEP = 0.15
OFFSET_STEP = 0.2


def setup():
    """Setup."""
    size(600, 600)


def draw():
    """Draw."""
    global FLYING
    stroke(255)
    background(0)
    noFill()

    FLYING -= FLYING_STEP

    yoff = FLYING
    for y in range(ROWS):
        xoff = 0
        for x in range(COLS):
            terrain[x, y] = map(simplex.noise2d(xoff, yoff), -1, 1, -40, 80)
            xoff += OFFSET_STEP
        yoff += OFFSET_STEP

    translate(width / 2, height / 2)
    rotateX(PI / 3)
    translate(-WIDTH / 2, -HEIGHT / 2)

    for y in range(0, ROWS - 1):
        beginShape(TRIANGLE_STRIP)
        for x in range(0, COLS):
            vertex(x * SCALE, y * SCALE, terrain[x, y])
            vertex(x * SCALE, (y + 1) * SCALE, terrain[x, y + 1])
        endShape()


run()
