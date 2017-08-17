import dialog
import draw
from maze import *
from os.path import isfile
from stopwatch import *

m = Maze()
sw = Stopwatch()

draw.menu("Which algorithm do you want to use?",
          Algorithm.Solve.DEPTH.value)

algorithm_count = 1
algorithm = dialog.user_input(1, algorithm_count, range_=True)

if algorithm == 1:
    algorithm = Algorithm.Solve.DEPTH
draw.line()

if isfile("maze.png"):
    print("Loading maze...")
    sw.start()
    m.load_maze_from_png()
    sw.stop()
    sw.print_elapsed_time()

    draw.line()

    print("Solving maze...")
    sw.start()
    m.solve(0, 0, algorithm)
    sw.stop()
    sw.print_elapsed_time()

    draw.line()
    print("Saving solution...")
    sw.start()
    m.save_solution_as_png()
    sw.stop()
    sw.print_elapsed_time()
else:
    draw.line()
    print("No maze.png found!")

draw.line()
dialog.enter("exit")

