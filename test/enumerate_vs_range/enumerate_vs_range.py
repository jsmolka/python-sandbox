from stopwatch import *

sw_enum = Stopwatch()
sw_range = Stopwatch()

l = list()
for i in range(0, 10000):
    l.append(i)

sw_enum.start()
for i in range(0, 10000):
    for j, e in enumerate(l):
        pass
sw_enum.stop()

sw_range.start()
for i in range(0, 10000):
    for j in range(0, len(l)):
        pass
sw_range.stop()

sw_range.print_elapsed_time(message="Elapsed time for range:")
sw_enum.print_elapsed_time(message="Elapsed time for enum:")
