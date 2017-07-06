import numpy as np
from stopwatch import *

l = [0] * 10
print(l)

x = 5
l = [1 if x == 0 else x for x in l]
print(l)
print(x)

l = [0 for x in l]
print(l)

l1 = [0] * 100000
sw1 = Stopwatch()
sw1.start()
a = np.array(l1)
a.fill(1)
sw1.stop()
sw1.print_elapsed_time()

sw2 = Stopwatch()
sw2.start()
l2 = [0] * 100000
l2 = [1] * 100000
sw2.stop()
sw2.print_elapsed_time()
