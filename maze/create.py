import cli
import stopwatch as sw
from maze import Maze

if __name__ == "__main__":
    print("Enter rows!")
    row_count = int(input())
    print("Enter columns!")
    col_count = int(input())

    cli.line()

    algorithms = [
        Maze.Create.C,
        Maze.Create.BACKTRACKING,
        Maze.Create.HUNT,
        Maze.Create.ELLER,
        Maze.Create.SIDEWINDER,
        Maze.Create.PRIM,
        Maze.Create.KRUSKAL
    ]

    index = cli.menu("Which algorithm do you want to use?", *[algorithm.value for algorithm in algorithms], result=True)
    algorithm = algorithms[index]

    cli.line()

    print("Creating maze...")
    sw = sw.Stopwatch()
    m = Maze()
    sw.start()
    m.create(row_count, col_count, algorithm)
    sw.stop()
    print(sw.elapsed_str)

    cli.line()
    print("Saving maze...")
    sw.start()
    m.save_maze()
    sw.stop()
    print(sw.elapsed_str)

    cli.line()
    cli.enter("exit")
