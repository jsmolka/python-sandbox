import dialog
import draw
from maze import *
from stopwatch import *

print("Enter scale!")
scale = int(input())

draw.line()
print("Loading maze...")
sw = Stopwatch()
sw.start()
m = CMaze()
m.load_maze_from_png()
sw.stop()
print(sw.elapsed_str)

draw.line()
print("Solving maze...")
sw.start()
m.solve(0, 0)
sw.stop()
print(sw.elapsed_str)

draw.line()
print("Saving solution...")
sw.start()
m.save_solution_as_png(scale=scale)
sw.stop()
print(sw.elapsed_str)



draw.line()
dialog.enter("exit")
