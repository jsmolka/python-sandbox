import numpy as np
from pyprocessing import *
from opensimplex import *

# Configuration
WIDTH = 1100
HEIGHT = 900
scl = 25
rows = round(HEIGHT / scl)
cols = round(WIDTH / scl)
terrain = np.zeros((cols, rows))
simplex = OpenSimplex()
flying = 0
flying_step = 0.15
offset_step = 0.2


def setup():
    size(600, 600)


def draw():
    global flying
    stroke(255)
    background(0)
    noFill()

    flying -= flying_step

    yoff = flying
    for y in range(0, rows):
        xoff = 0
        for x in range(0, cols):
            terrain[x, y] = map(simplex.noise2d(xoff, yoff), -1, 1, -40, 80)
            xoff += offset_step
        yoff += offset_step

    translate(width / 2, height / 2)
    rotateX(PI / 3)
    translate(-WIDTH / 2, -HEIGHT / 2)

    for y in range(0, rows - 1):
        beginShape(TRIANGLE_STRIP)
        for x in range(0, cols):
            vertex(x * scl, y * scl, terrain[x, y])
            vertex(x * scl, (y + 1) * scl, terrain[x, y + 1])
        endShape()


run()
