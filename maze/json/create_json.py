from maze import *

m = Maze()

print("Enter rows!")
rows = int(input())
print("Enter columns!")
cols = int(input())

m.create(rows, cols, Algorithm.Create.BACKTRACKING)
m.save_maze_as_json()
m.solve(0, 0, Algorithm.Solve.DEPTH)
m.save_solution_as_json()
