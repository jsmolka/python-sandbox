import numpy as np
from pyprocessing import *
from PIL import Image

arr = np.zeros((100, 100, 3), dtype=np.uint8)
precision = 10

for x in range(0, 100):
    for y in range(0, 100):
        value = map(noise(x / precision, y / precision), -1, 1, 0, 255)
        arr[x, y] = [value, value, value]

img = Image.fromarray(arr, "RGB")
img.save("perlin_noise.png", "PNG")
