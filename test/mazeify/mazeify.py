import numpy as np
from PIL import Image


def maze_shape(array):
    """Resizes an array to maze shape"""
    shape = arr.shape
    return np.resize(arr, (2 * (shape[0] // 2) + 1, 2 * (shape[1] // 2) + 1, 3))

def change_color(array, new_white, new_rest):
    """Changes color of an array"""
    shape = arr.shape
    arr.flatten()
    arr[arr < 255] = new_rest
    arr[arr == 255] = new_white
    arr.shape = shape
    return arr

arr = np.array(Image.open("src.png"), dtype=np.uint8)
arr = maze_shape(arr)
arr = change_color(arr, 0, 1)
Image.fromarray(arr, "RGB").save("res.png", "png")
