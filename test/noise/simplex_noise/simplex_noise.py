import numpy as np
from PIL import Image
from opensimplex import *

# Noise image

WIDTH = 512
HEIGHT = 512
FEATURE_SIZE = 100

simplex = OpenSimplex()
print("Generating 2D image...")
img = Image.new("L", (WIDTH, HEIGHT))
for y in range(0, HEIGHT):
    for x in range(0, WIDTH):
        value = simplex.noise2d(x / FEATURE_SIZE, y / FEATURE_SIZE)
        color = int((value + 1) * 128)
        img.putpixel((x, y), color)
img.save("noise_pixel.png")

# Noise rgb array

print("Generating RGB array...")
arr = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
for i in range(0, HEIGHT):
    for j in range(0, WIDTH):
        value = simplex.noise2d(i / FEATURE_SIZE, j / FEATURE_SIZE)
        color = int((value + 1) * 128)
        arr[i, j] = [color, color, color]

img = Image.fromarray(arr, "RGB")
img.save("noise_array.png")

