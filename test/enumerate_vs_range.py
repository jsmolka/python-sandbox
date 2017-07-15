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
sw.print_elapsed_time(message="Elapsed time for enumerate:")

sw.reset()

sw.start()
for i in range(0, 10000):
    for j in range(0, len(l)):
        pass
sw.stop()
sw.print_elapsed_time(message="Elapsed time for range:")

dialog.enter("exit")
