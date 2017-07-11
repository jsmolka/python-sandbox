import dialog
import draw
from maze import *
from stopwatch import *

m = Maze()
sw = Stopwatch()

draw.menu("Which algorithm do you want to use?",
          Algorithm.Solve.BACKTRACKING.value)

algorithm_count = 1
algorithm = dialog.user_input(1, algorithm_count + 1, create_range=True)

if algorithm == 1:
    algorithm = Algorithm.Solve.BACKTRACKING
draw.line()

if os.path.isfile("maze.png"):
    print("Loading maze...")
    sw.start()
    m.load_maze_from_png()
    sw.stop()
    sw.print_elapsed_time()

    draw.line()

    print("Solving maze...")
    sw.start()
    m.solve(0, 0, Algorithm.Solve.BACKTRACKING)
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

