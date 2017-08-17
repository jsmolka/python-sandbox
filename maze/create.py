import dialog
import draw
from maze import *
from stopwatch import *

print("Enter rows!")
row_count = int(input())
print("Enter columns!")
col_count = int(input())

draw.line()

draw.menu("Which algorithm do you want to use?",
          Algorithm.Create.BACKTRACKING.value,
          Algorithm.Create.HUNT.value,
          Algorithm.Create.ELLER.value,
          Algorithm.Create.SIDEWINDER.value,
          Algorithm.Create.PRIM.value,
          Algorithm.Create.KRUSKAL.value)

algorithm_count = 6
algorithm = dialog.user_input(1, algorithm_count, range_=True)

if algorithm == 1:
    algorithm = Algorithm.Create.BACKTRACKING
elif algorithm == 2:
    algorithm = Algorithm.Create.HUNT
elif algorithm == 3:
    algorithm = Algorithm.Create.ELLER
elif algorithm == 4:
    algorithm = Algorithm.Create.SIDEWINDER
elif algorithm == 5:
    algorithm = Algorithm.Create.PRIM
elif algorithm == 6:
    algorithm = Algorithm.Create.KRUSKAL

draw.line()

print("Creating maze...")
sw = Stopwatch()
m = Maze()
sw.start()
m.create(row_count, col_count, algorithm)
sw.stop()
sw.print_elapsed_time()

draw.line()
print("Saving maze...")
sw.start()
m.save_maze_as_png()
sw.stop()
sw.print_elapsed_time()

draw.line()
dialog.enter("exit")
