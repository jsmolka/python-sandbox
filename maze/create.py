from cli import *
from maze import *
from stopwatch import *

print("Enter rows!")
row_count = int(input())
print("Enter columns!")
col_count = int(input())

line()

algorithms = [
    Maze.Create.C,
    Maze.Create.BACKTRACKING,
    Maze.Create.HUNT,
    Maze.Create.ELLER,
    Maze.Create.SIDEWINDER,
    Maze.Create.PRIM,
    Maze.Create.KRUSKAL
]

index = menu("Which algorithm do you want to use?", *[algorithm.value for algorithm in algorithms], result=True)
algorithm = algorithms[index]

line()

print("Creating maze...")
sw = Stopwatch()
m = Maze()
sw.start()
m.create(row_count, col_count, algorithm)
sw.stop()
print(sw.elapsed_str)

line()
print("Saving maze...")
sw.start()
m.save_maze_as_png()
sw.stop()
print(sw.elapsed_str)

line()
enter("exit")
