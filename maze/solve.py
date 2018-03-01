import cli
import stopwatch as sw
from maze import Maze

if __name__ == "__main__":
    m = Maze()
    sw = sw.Stopwatch()

    algorithms = [
        Maze.Solve.C,
        Maze.Solve.DEPTH,
        Maze.Solve.BREADTH
    ]

    index = cli.menu("Which algorithm do you want to use?", *[algorithm.value for algorithm in algorithms], result=True)
    algorithm = algorithms[index]

    cli.line()

    print("Loading maze...")
    sw.start()
    m.load_maze()
    sw.stop()
    print(sw.elapsed_str)

    cli.line()

    print("Solving maze...")
    sw.start()
    m.solve((), (), algorithm)
    sw.stop()
    print(sw.elapsed_str)

    cli.line()
    print("Saving solution...")
    sw.start()
    m.save_solution()
    sw.stop()
    print(sw.elapsed_str)

    cli.line()
    cli.enter("exit")
