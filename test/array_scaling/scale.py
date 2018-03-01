import numpy as np
import random
from PIL import Image

if __name__ == "__main__":
    H = 10
    W = 10

    arr = np.zeros((H, W), dtype=np.uint8)
    for x in range(H):
        for y in range(W):
            if random.getrandbits(1):
                arr[x, y] = 255

    SX = 5
    SY = 5

    arr = arr.reshape((H, W, 1))  # Reshape to get 3rd dimension
    arr = arr.repeat(SX, axis=0).repeat(SY, axis=1).repeat(3, axis=2)  # Scale up
    Image.fromarray(arr, "RGB").save("up.png", "png")
    arr = arr[::SX, ::SY]  # Scale down
    Image.fromarray(arr, "RGB").save("down.png", "png")
    arr = arr[:, :, ::3]  # Scale rgb part down
    arr = arr.reshape((H, W))  # Get original form
