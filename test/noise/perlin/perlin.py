import numpy as np
import dialog
import utils
from pyprocessing import mathfunctions
from PIL import Image

PRECISION = 10

print("Generating noise...")
arr = np.zeros((100, 100, 3), dtype=np.uint8)
for x in range(0, 100):
    for y in range(0, 100):
        value = utils.remap(mathfunctions.noise(x / PRECISION, y / PRECISION), -1, 1, 0, 255)
        arr[x, y] = [value, value, value]

img = Image.fromarray(arr, "RGB")
img.save("noise.png", "PNG")

dialog.enter("exit")
