import dialog
import itertools
import math
import numpy as np


def __permutations(permutation_list):
    """Creates permutations"""
    permutation_object = itertools.permutations(permutation_list)
    permutations = np.zeros((math.factorial(len(permutation_list)), len(permutation_list)), dtype=np.uint8)
    for i, permutation in enumerate(permutation_object):
        permutations[i] = permutation
    return permutations


def hamiltonian_path(node_count, edges):
    """Calculates hamiltonian path"""
    permutations = list()
    for i in range(1, node_count + 1):  # Create list of nodes
        permutations.append(i)
    for edge in edges:  # Add reversed edges to edges
        reverse_edge = (edge[1], edge[0])
        if reverse_edge not in edges:
            edges.append(reverse_edge)

    # Create permutations
    permutations = __permutations(permutations)

    # Calculate hamiltonian path
    result = list()
    for path in permutations:
        should_add = True
        for i in range(0, node_count - 1):
            if (path[i], path[i + 1]) not in edges:
                should_add = False
                break
        if should_add:
            result.append(path)
    return result


if __name__ == "__main__":
    e = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (3, 6), (4, 5), (4, 7), (5, 6), (6, 7)]
    p = hamiltonian_path(7, e)
    for l in p:
        print(l)

    dialog.enter("exit")
