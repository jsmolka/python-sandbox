import numpy as np
import cli
import itertools

if __name__ == "__main__":
    n = int(input("Range: "))

    perm_object = itertools.permutations(list(range(1, n + 1)))
    arr = np.array([list(perm) for perm in perm_object])

    print(arr)

    cli.enter("exit")
