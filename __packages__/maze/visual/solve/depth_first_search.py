from maze import *
from pyprocessing import *

# Configuration
row_count = 35
col_count = 35
scale = 8
start = 0  # Top left corner if zero
end = 0  # Bottom right corner if zero
create_algorithm = Algorithm.Create.BACKTRACKING

# Define variables
m = Maze()
m.create(row_count, col_count, create_algorithm)
row_count_with_walls = 2 * row_count + 1
col_count_with_walls = 2 * col_count + 1

visited_cells = m.maze.copy()  # List of visited cells, value of visited cell is [0, 0, 0]
stack = []  # List of visited cells [(x, y), ...]

# Define start and end
if start == 0:
    start = (0, 0)
if end == 0:
    end = (row_count - 1, col_count - 1)
start = tuple([2 * x + 1 for x in start])
end = tuple([2 * x + 1 for x in end])

x, y = start
visited_cells[x, y] = [0, 0, 0]
stack.append((x, y))

current_cells = []  # List of cells [(x, y), ...]
last_cells = []  # List of cells [(x, y), ...]
current_cells.append((x, y))

walking = True
found = False
first_time = True

s_dir_one = [
    lambda x, y: (x + 1, y),
    lambda x, y: (x - 1, y),
    lambda x, y: (x, y - 1),
    lambda x, y: (x, y + 1)
]

dir_two = [
    lambda x, y: (x + 2, y, x + 1, y),
    lambda x, y: (x - 2, y, x - 1, y),
    lambda x, y: (x, y - 2, x, y - 1),
    lambda x, y: (x, y + 2, x, y + 1)
]


def walk():
    """Walks over maze"""
    global x, y, stack, visited_cells, walking, first_time, current_cells
    for direction in dir_two:  # Check adjacent cells
        tx, ty, bx, by = direction(x, y)
        if visited_cells[bx, by, 0] == 255:  # Check if unvisited
            visited_cells[bx, by] = visited_cells[tx, ty] = [0, 0, 0]  # Mark as visited
            stack.append((tx, ty))
            current_cells.append((bx, by))
            x, y, walking = tx, ty, True
            return  # Return new cell and continue walking
    walking, first_time = False, True


def backtrack():
    """Backtracks stack"""
    global x, y, stack, visited_cells, walking, first_time
    if first_time:  # Compensate for first backtrack after walking
        first_time = False
        backtrack()
    x, y = stack.pop()
    for direction in s_dir_one:  # Check adjacent cells
        tx, ty = direction(x, y)
        if visited_cells[tx, ty, 0] == 255:  # Check if unvisited
            stack.append((x, y))
            walking = True
            return  # Return cell with unvisited neighbour


def draw_maze():
    """Draws maze"""
    global m, row_count_with_walls, col_count_with_walls, scale
    fill(255)
    for x in range(0, row_count_with_walls):
        for y in range(0, col_count_with_walls):
            if m.maze[x, y, 0] == 255:
                rect(y * scale, x * scale, scale, scale)


def color(iteration_):
    """Returns color for current iteration"""
    global offset
    return [0 + (iteration_ * offset), 0, 255 - (iteration_ * offset)]


def draw_stack():
    """Draws stack"""
    global x, y, offset, iteration, scale
    if iteration < len(stack) - 1:  # Draw incomplete stack
        x1, y1 = tuple(stack[iteration])
        x2, y2 = tuple(stack[iteration + 1])
        r, g, b = color(2 * iteration)
        fill(r, g, b)
        rect(y1 * scale, x1 * scale, scale, scale)
        x3, y3 = int((x1 + x2) / 2), int((y1 + y2) / 2)
        r, g, b = color(2 * iteration + 1)
        fill(r, g, b)
        rect(y3 * scale, x3 * scale, scale, scale)
    else:
        x, y = tuple(stack[-1])
        r, g, b = color(2 * (len(stack) - 1))
        fill(r, g, b)
        rect(y * scale, x * scale, scale, scale)
    if iteration == len(stack):
        noLoop()
    iteration += 1


def draw_cells():
    """Draws cells"""
    global found, current_cells, last_cells, scale
    fill(0, 255, 0)
    for x, y in current_cells:
        rect(y * scale, x * scale, scale, scale)
    fill(128)
    for x, y in last_cells:
        rect(y * scale, x * scale, scale, scale)
    if found:
        fill(128)
        for x, y in current_cells:
            rect(y * scale, x * scale, scale, scale)
    current_cells, last_cells = [], current_cells


def setup():
    global row_count_with_walls, col_count_with_walls, scale
    size(col_count_with_walls * scale, row_count_with_walls * scale, caption=Algorithm.Solve.DEPTH.value)
    background(0)
    noStroke()
    draw_maze()


def draw():
    global x, y, stack, offset, iteration, end, walking, found, current_cells
    if not found:
        if walking:
            walk()
        else:
            backtrack()
        current_cells.append((x, y))
        if (x, y) == end:  # Stop at end
            found = True
            offset, iteration = 255 / (2 * len(stack)), 0
        draw_cells()
    else:
        draw_stack()


run()