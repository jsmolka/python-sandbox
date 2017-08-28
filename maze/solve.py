import dialog
import draw
from maze import *
from os.path import isfile
from stopwatch import *

m = Maze()
sw = Stopwatch()

algorithms = [
    Algorithm.Solve.DEPTH,
    Algorithm.Solve.BREADTH
]

draw.menu("Which algorithm do you want to use?",
          [algorithm.value for algorithm in algorithms])

index = dialog.user_input(1, len(algorithms), range_=True)

algorithm = algorithms[index - 1]
draw.line()

if isfile("maze.png"):
    print("Loading maze...")
    sw.start()
    m.load_maze_from_png()
    sw.stop()
    print(sw.elapsed_str)

    draw.line()

    print("Solving maze...")
    sw.start()
    m.solve(0, 0, algorithm)
    sw.stop()
    print(sw.elapsed_str)

    draw.line()
    print("Saving solution...")
    sw.start()
    m.save_solution_as_png()
    sw.stop()
    print(sw.elapsed_str)
else:
    draw.line()
    print("No maze.png found!")

draw.line()
dialog.enter("exit")
