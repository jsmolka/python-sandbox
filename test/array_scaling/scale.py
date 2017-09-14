import numpy as np
from PIL import Image
from random import getrandbits

H = 10
W = 10

n = np.zeros((H, W), dtype=np.uint8)
for x in range(0, H):
    for y in range(0, W):
        if getrandbits(1):
            n[x, y] = 255

SX = 5
SY = 5


n = n.reshape((H, W, 1))  # Reshape to get 3rd dimension
n = n.repeat(SX, axis=0).repeat(SY, axis=1).repeat(3, axis=2)  # Scale up
Image.fromarray(n, "RGB").save("up.png", "png")
n = n[::SX, ::SY]  # Scale down
Image.fromarray(n, "RGB").save("down.png", "png")
n = n[:, :, ::3]  # Scale rgb part down
n = n.reshape((H, W))  # Get original form
