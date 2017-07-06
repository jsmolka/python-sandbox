import numpy as np
import dialog
from stopwatch import *
from pyprocessing import *
from opensimplex import *
from PIL import Image

sw = Stopwatch()

arr1 = np.zeros((1000, 1000, 3), dtype=np.uint8)
arr2 = np.zeros((1000, 1000, 3), dtype=np.uint8)

precision = 10

print("Generating simplex noise...")
simplex = OpenSimplex()
sw.start()
for x in range(0, 1000):
    for y in range(0, 1000):
        value = map(simplex.noise2d(x / precision, y / precision), -1, 1, 0, 255)
        arr1[x, y] = [value, value, value]
sw.stop()
sw.print_elapsed_time()

print("Generating perlin noise...")
sw.start()
for x in range(0, 1000):
    for y in range(0, 1000):
        value = map(noise(x / precision, y / precision), -1, 1, 0, 255)
        arr2[x, y] = [value, value, value]
sw.stop()
sw.print_elapsed_time()

print("Saving images...")
img1 = Image.fromarray(arr1, "RGB")
img1.save("simplex_noise.png", "PNG")

img2 = Image.fromarray(arr2, "RGB")
img2.save("perlin_noise.png", "PNG")

dialog.enter("exit")
