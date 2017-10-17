from cli import *
from maze import *
from os.path import isfile
from stopwatch import *

m = Maze()
sw = Stopwatch()

algorithms = [
    Algorithm.Solve.C,
    Algorithm.Solve.DEPTH,
    Algorithm.Solve.BREADTH
]

menu("Which algorithm do you want to use?", *[algorithm.value for algorithm in algorithms])

index = user_input(1, len(algorithms), span=True)

algorithm = algorithms[index - 1]
line()

if isfile("maze.png"):
    print("Loading maze...")
    sw.start()
    m.load_maze_from_png()
    sw.stop()
    print(sw.elapsed_str)

    line()

    print("Solving maze...")
    sw.start()
    m.solve(0, 0, algorithm)
    sw.stop()
    print(sw.elapsed_str)

    line()
    print("Saving solution...")
    sw.start()
    m.save_solution_as_png()
    sw.stop()
    print(sw.elapsed_str)
else:
    line()
    print("No maze.png found!")

line()
enter("exit")
