from cli import *


def ackermann_recursive(m, n):
    """Calculates the Ackermann function recursively"""
    global calls
    calls += 1
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann_recursive(m - 1, 1)
    else:
        return ackermann_recursive(m - 1, ackermann_recursive(m, n - 1))


def ackermann_while(m, n):
    """Calculates the Ackerman function with a while loop"""
    global calls
    calls += 1
    while m != 0:
        if n == 0:
            n = 1
        else:
            n = ackermann_while(m, n - 1)
        m -= 1
    return n + 1


if __name__ == "__main__":
    heading("Ackermann recursive")
    for i in range(1, 4):
        for j in range(1, 4):
            calls = 0
            print("ackermann({0}, {1}) =".format(i, j), ackermann_recursive(i, j), "|", "Calls:", calls)
    heading("Ackermann while")
    for i in range(1, 4):
        for j in range(1, 4):
            calls = 0
            print("ackermann({0}, {1}) =".format(i, j), ackermann_while(i, j), "|", "Calls:", calls)

    line(style=LineStyle.HASH)
    enter("exit")
