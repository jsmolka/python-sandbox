import numpy as np

def to_3d(idx):
    """Converts 1d index to 3d index"""
    z = idx % D
    y = ((idx - z) // D) % W
    x = int((idx - z - D * y) / (W * D))
    return x, y, z


def to_1d(x, y, z):
    """Converts 3d index to 1d index"""
    # return x * W * D + y * D + z
    return (x * W + y) * D + z


H = 5
W = 5
D = 3

for i in range(0, H):
    for j in range(0, W):
        for k in range(0, D):
            idx = to_1d(i, j, k)
            x, y, z = to_3d(idx)
            print((i, j, k), idx, (x, y, z))
