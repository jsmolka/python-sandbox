from cli import *
from maze import *
from stopwatch import *

print("Enter rows!")
row_count = int(input())
print("Enter columns!")
col_count = int(input())

line()

algorithms = [
    Algorithm.Create.C,
    Algorithm.Create.BACKTRACKING,
    Algorithm.Create.HUNT,
    Algorithm.Create.ELLER,
    Algorithm.Create.SIDEWINDER,
    Algorithm.Create.PRIM,
    Algorithm.Create.KRUSKAL
]

menu("Which algorithm do you want to use?", *[algorithm.value for algorithm in algorithms])

index = user_input(1, len(algorithms), span=True)

algorithm = algorithms[index - 1]
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
