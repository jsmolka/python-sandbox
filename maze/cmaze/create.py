import dialog
import draw
from maze import *
from stopwatch import *

print("Enter rows!")
row_count = int(input())
print("Enter columns!")
col_count = int(input())
print("Enter scale!")
scale = int(input())

draw.line()

print("Creating maze...")
sw = Stopwatch()
m = CMaze()
sw.start()
m.create(row_count, col_count)
sw.stop()
print(sw.elapsed_str)

draw.line()
print("Saving maze...")
sw.start()
m.save_maze_as_png(scale=scale)
sw.stop()
print(sw.elapsed_str)

draw.line()
dialog.enter("exit")
