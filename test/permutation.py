import dialog
import itertools
import numpy as np

print("Input number for permutations")
n = int(input())

l = list()
for i in range(1, n + 1):
    l.append(i)

perm_object = itertools.permutations(l)
p = list()
for perm in perm_object:
    p.append(perm)
a = np.array(p)

print("Array: ", a)  # Returns list of lists
print("List: ", p)  # Returns list of tuples

dialog.enter("exit")
