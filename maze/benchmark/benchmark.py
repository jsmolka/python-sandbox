import dialog
import draw
from database import *
from maze import *
from stopwatch import *

# Load data
db = Database("data.json")

method_list = [
    "Create",
    "Solve",
]
draw.menu("Which method do you want to benchmark?", method_list)

method = dialog.user_input(1, len(method_list))

draw.line()
if method == 1:
    algorithm_list = [
        Algorithm.Create.BACKTRACKING.value,
        Algorithm.Create.HUNT.value,
        Algorithm.Create.ELLER.value,
        Algorithm.Create.SIDEWINDER.value,
        Algorithm.Create.PRIM.value,
        Algorithm.Create.KRUSKAL.value
    ]

    draw.menu("Which algorithm do you want to use?", algorithm_list)

    algorithm = dialog.user_input(1, len(algorithm_list), range_=True)

    if algorithm == 1:
        algorithm = Algorithm.Create.BACKTRACKING
    elif algorithm == 2:
        algorithm = Algorithm.Create.HUNT
    elif algorithm == 3:
        algorithm = Algorithm.Create.ELLER
    elif algorithm == 4:
        algorithm = Algorithm.Create.SIDEWINDER
    elif algorithm == 5:
        algorithm = Algorithm.Create.PRIM
    elif algorithm == 6:
        algorithm = Algorithm.Create.KRUSKAL

    # Input data
    draw.line()
    print("Which version are you testing?")
    version = input()

    draw.line()
    print("Which system are you using? (PC/XPS)")
    system = dialog.user_input("PC", "XPS")

    draw.line()
    print("How many times do you want to repeat the benchmark?")
    iteration = int(input())

    draw.line()
    print("How many rows should the maze have?")
    row_count = int(input())

    draw.line()
    print("How many columns should the maze have?")
    col_count = int(input())

    # Benchmark
    draw.line()
    sw = Stopwatch()
    m = Maze()
    draw.progress_bar(0, iteration, "Benchmark progress:")
    sw.start()
    for i in range(0, iteration):
        m.create(row_count, col_count, algorithm)
        sw.round()
        draw.progress_bar(i + 1, iteration, "Benchmark progress:")
    sw.stop()

    # Print result
    draw.line()
    sw.print_average_time()

    # Add data
    size = "{0} x {1}".format(row_count, col_count)
    db.add("create", algorithm.value, version, system, str(iteration), size, str(sw.average_time))
else:
    algorithm_list = [
        Algorithm.Solve.DEPTH.value
    ]

    draw.menu("Which algorithm do you want to use?", algorithm_list)

    algorithm = dialog.user_input(1, len(algorithm_list), range_=True)

    if algorithm == 1:
        algorithm = Algorithm.Solve.DEPTH

    # Input data
    draw.line()
    print("Which version are you testing?")
    version = input()

    draw.line()
    print("Which system are you using? (PC/XPS)")
    system = dialog.user_input("PC", "XPS")

    draw.line()
    print("How many times do you want to repeat the benchmark?")
    iteration = int(input())

    draw.line()
    print("How many rows should the maze have?")
    row_count = int(input())

    draw.line()
    print("How many columns should the maze have?")
    col_count = int(input())

    draw.line()

    # Benchmark
    sw = Stopwatch()
    m = Maze()
    total_time = timedelta(0, 0)
    draw.progress_bar(0, iteration, "Benchmark progress:")
    for i in range(0, iteration):
        m.create(row_count, col_count, Algorithm.Create.BACKTRACKING)
        sw.start()
        m.solve(0, 0, algorithm)
        sw.stop()
        total_time += sw.elapsed_time
        draw.progress_bar(i + 1, iteration, "Benchmark progress:")

    # Print result
    draw.line()
    average_time = total_time / iteration
    print("Average time for {0} rounds: {1}".format(iteration, average_time))

    # Add data
    size = "{0} x {1}".format(row_count, col_count)
    db.add("solve", algorithm.value, version, system, str(iteration), size, str(average_time))

# Save to JSON
db.save("data.json")

draw.line()
dialog.enter("exit")
