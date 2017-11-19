from cli import *
from database import *
from maze import *
from stopwatch import *


class Data:
    def __init__(self):
        self.name = None
        self.version = None
        self.system = None
        self.iterations = None
        self.size = None
        self.time = None


db = Database("data.json")

algorithms_create = [
    Algorithm.Create.BACKTRACKING,
    Algorithm.Create.HUNT,
    Algorithm.Create.ELLER,
    Algorithm.Create.SIDEWINDER,
    Algorithm.Create.PRIM,
    Algorithm.Create.KRUSKAL
]

algorithms_solve = [
    Algorithm.Solve.DEPTH,
    Algorithm.Solve.BREADTH
]

algorithms_all = []
algorithms_all.extend(algorithms_create)
algorithms_all.extend(algorithms_solve)

index = menu("Which algorithm do you want to use?", *[algorithm.value for algorithm in algorithms_all], result=True)
algorithm = algorithms_all[index]

data = Data()
data.name = algorithm.value

line()
print("Which version are you testing?")
data.version = input()

line()
print("Which system are you using? (PC/XPS)")
data.system = user_input("PC", "XPS")

line()
print("How many times do you want to repeat the benchmark?")
data.iterations = int(input())

line()
print("How many rows should the maze have?")
row_count = int(input())

line()
print("How many columns should the maze have?")
col_count = int(input())
data.size = "{0} x {1}".format(row_count, col_count)

line()
sw = Stopwatch()
m = Maze()
progress_bar(0, data.iterations, "Benchmark progress:")

if algorithm in algorithms_create:
    sw.start()
    for i in range(0, data.iterations):
        m.create(row_count, col_count, algorithm)
        sw.round()
        progress_bar(i + 1, data.iterations, "Benchmark progress:")
    sw.stop()

    line()
    print(sw.average_str)
    data.time = str(sw.average)
else:
    total_time = timedelta(0, 0)
    for i in range(0, data.iterations):
        m.create(row_count, col_count, Algorithm.Create.BACKTRACKING)
        sw.start()
        m.solve(0, 0, algorithm)
        sw.stop()
        total_time += sw.elapsed
        progress_bar(i + 1, data.iterations, "Benchmark progress:")

    line()
    average_time = total_time / data.iterations
    print("Average time for {0} rounds: {1}".format(data.iterations, average_time))
    data.time = str(average_time)

db.add(data)
db.save()

line()
enter("exit")
