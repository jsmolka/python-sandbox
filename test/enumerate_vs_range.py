import dialog
from stopwatch import *

sw = Stopwatch()

l = list()
for i in range(0, 10000):
    l.append(i)

sw.start()
for i in range(0, 10000):
    for j, e in enumerate(l):
        pass
sw.stop()
print("Elapsed time for enumerate: " + str(sw.elapsed))

sw.reset()

sw.start()
for i in range(0, 10000):
    for j in range(0, len(l)):
        pass
sw.stop()
print("Elapsed time for range: " + str(sw.elapsed))

dialog.enter("exit")
