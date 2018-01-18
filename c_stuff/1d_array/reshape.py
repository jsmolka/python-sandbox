import numpy as np


def index_2d(x, y):
    """Converts 2d index to 1d index"""
    return x * W + y


def index_3d(x, y, z):
    """Converts 3d index to 1d index"""
    # return x * W * D + y * D + z
    return (x * W + y) * D + z


H = 7
W = 8
D = 9

n = np.array(range(H * W * D))
n = n.reshape((H, W, D))
n = n.flatten()

print("def", index_3d(4, 4, 4))
print("n1", index_3d(5, 4, 4))  # + D * W
print("s1", index_3d(3, 4, 4))  # - D * W
print("e1", index_3d(4, 5, 4))  # + D
print("w1", index_3d(4, 3, 4))  # - D
