import dialog
import draw
from database import *
from maze import *

# Load data
db = Database("data.json")

algorithms = [
    Algorithm.Create.BACKTRACKING.value,
    Algorithm.Create.HUNT.value,
    Algorithm.Create.ELLER.value,
    Algorithm.Create.SIDEWINDER.value,
    Algorithm.Create.PRIM.value,
    Algorithm.Create.KRUSKAL.value,

    Algorithm.Solve.DEPTH.value,
    Algorithm.Solve.BREADTH.value
]

draw.menu("Which algorithm do you want to display?", algorithms)
index = dialog.user_input(1, len(algorithms), range_=True) - 1
algorithm = algorithms[index]

draw.heading(algorithm)

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

draw.line()

dialog.enter("exit")
