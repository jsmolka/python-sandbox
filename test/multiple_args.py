from cli import *


def defy(*args):
    """Test function"""
    print(type(args))
    for arg in args:
        print(arg)


defy(1, 2, 3, 4)

enter("exit")
