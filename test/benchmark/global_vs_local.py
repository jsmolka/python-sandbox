from benchmark import *


def func(c):
    return c


def local_(c):
    l = func
    for i in range(0, c):
        l(i)


def global_(c):
    for i in range(0, c):
        func(i)


compare(local_, global_, 50000, 50000, 100)
input()
