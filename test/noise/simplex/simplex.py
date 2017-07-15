import numpy as np
import dialog
from PIL import Image
from opensimplex import *

WIDTH = 512
HEIGHT = 512
FEATURE_SIZE = 100

print("Generating noise...")
simplex = OpenSimplex()
arr = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
for i in range(0, HEIGHT):
    for j in range(0, WIDTH):
        value = simplex.noise2d(i / FEATURE_SIZE, j / FEATURE_SIZE)
        color = int((value + 1) * 128)
        arr[i, j] = [color, color, color]

img = Image.fromarray(arr, "RGB")
img.save("noise.png")

dialog.enter("exit")
