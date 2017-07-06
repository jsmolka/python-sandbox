import dialog
import draw
from database import *
from maze import *

# Load data
db = Database("data.json")

draw.menu("Which results do you want to display?",
          "Create",
          "Solve")

method = dialog.user_input(1, 2)

if method == 1:  # Show create
    algorithm_list = [
        Algorithm.Create.BACKTRACKING.value,
        Algorithm.Create.HUNT.value,
        Algorithm.Create.ELLER.value,
        Algorithm.Create.SIDEWINDER.value,
        Algorithm.Create.PRIM.value,
        Algorithm.Create.KRUSKAL.value
    ]
    method = "create"
else:  # Show solve
    algorithm_list = [
        Algorithm.Solve.BACKTRACKING.value
    ]
    method = "solve"

for algorithm in algorithm_list:
    draw.heading(algorithm)
    value_list = db.filter(algorithm, method)

    for value in value_list:
        iteration = value[4]
        if len(iteration) == 1:
            iteration = "  {0}".format(iteration)
        elif len(iteration) == 2:
            iteration = " {0}".format(iteration)
        system = value[3]
        if system == "PC":
            system = " PC"

        print("Version: {0} | system: {1} | iterations: {2} | size: {3} | average time: {4}".format(
            value[2],
            system,
            iteration,
            value[5],
            value[6]
        ))

    print("\n")

dialog.enter("exit")
