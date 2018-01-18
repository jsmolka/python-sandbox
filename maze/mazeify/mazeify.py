import numpy as np
from PIL import Image


def maze_shape(array):
    """Resizes an array to maze shape"""
    shape = array.shape
    return np.resize(array, (2 * (shape[0] // 2) + 1, 2 * (shape[1] // 2) + 1, 3))


def purify(array, flip=False):
    """Purifies white and black color"""
    shape = array.shape
    array.flatten()
    if not flip:
        array[array < 128] = 128
        array[array > 128] = 255
        array[array == 128] = 0
    else:
        array[array > 128] = 128
        array[array < 128] = 255
        array[array == 128] = 0
    array.shape = shape
    return array


def change_color(array, new_white, new_rest):
    """Changes color of an array"""
    shape = array.shape
    array.flatten()
    array[array < 255] = new_rest
    array[array == 255] = new_white
    array.shape = shape
    return array


arr = np.array(Image.open("src.png"), dtype=np.uint8)
arr = maze_shape(purify(arr, flip=True))
Image.fromarray(arr, "RGB").save("res.png", "png")
