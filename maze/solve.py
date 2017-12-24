from cli import *
from maze import *
from os.path import isfile
from stopwatch import *

m = Maze()
sw = Stopwatch()

algorithms = [
    Maze.Solve.C,
    Maze.Solve.DEPTH,
    Maze.Solve.BREADTH
]

index = menu("Which algorithm do you want to use?", *[algorithm.value for algorithm in algorithms], result=True)
algorithm = algorithms[index]

line()

if isfile("maze.png"):
    print("Loading maze...")
    sw.start()
    m.load_maze()
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
    m.save_solution()
    sw.stop()
    print(sw.elapsed_str)
else:
    line()
    print("No maze.png found!")

line()
enter("exit")
