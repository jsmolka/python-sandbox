from maze import *

m = Maze()
m.load_maze_from_json()
m.load_solution_from_json()

m.save_maze_as_png()
m.save_solution_as_png()
