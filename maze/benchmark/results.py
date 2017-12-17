from cli import *
from database import *
from maze import *

# Load data
db = Database("data.json")

algorithms = [
    Maze.Create.BACKTRACKING.value,
    Maze.Create.HUNT.value,
    Maze.Create.ELLER.value,
    Maze.Create.SIDEWINDER.value,
    Maze.Create.PRIM.value,
    Maze.Create.KRUSKAL.value,

    Maze.Solve.DEPTH.value,
    Maze.Solve.BREADTH.value
]

index = menu("Which algorithm do you want to display?", *algorithms, result=True)
algorithm = algorithms[index]

heading(algorithm)

for result in db.filter(("name", algorithm)):
    result.iterations = str(result.iterations)
    if len(result.iterations) == 1:
        result.iterations = "  {0}".format(result.iterations)
    elif len(result.iterations) == 2:
        result.iterations = " {0}".format(result.iterations)
    if result.system == "PC":
        result.system = " PC"

    print("Version: {0} | system: {1} | iterations: {2} | size: {3} | time: {4}".format(
        result.version,
        result.system,
        result.iterations,
        result.size,
        result.time
    ))

line()

enter("exit")
