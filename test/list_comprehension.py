import numpy as np
import dialog
from stopwatch import *

l = [0] * 10
l[9] = 1
print(l)

l = [1 if x == 0 else 2 for x in l]
print(l)

l = [0 for x in l]
print(l)

l = [0] * 100000

print("List to array then fill():")
sw = Stopwatch()
sw.start()
a = np.array(l)
a.fill(1)
sw.stop()
sw.print_elapsed_time()

sw.reset()
print("Assign new list:")
sw.start()
l = [1] * 100000
sw.stop()
sw.print_elapsed_time()

sw.reset()
print("List comprehension:")
sw.start()
l = [0 for x in l]
sw.stop()
sw.print_elapsed_time()

dialog.enter("exit")
