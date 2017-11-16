import glob
import os
from random import shuffle
from subprocess import Popen, STDOUT, DEVNULL


def add_path(path, variable):
    """Adds path to system variable"""
    if variable in os.environ:
        if path not in os.environ[variable].split(";"):
            Popen(["setx", variable, os.environ.get(variable) + ";" + path], stdout=DEVNULL, stderr=STDOUT)
    else:
        Popen(["setx", variable, path], stdout=DEVNULL, stderr=STDOUT)


def create_class(name, fields):
    """Creates object dynamically"""
    class_ = type(name, (object,), {})
    for field in fields:
        setattr(class_, field, None)
    return class_


def my_dict(obj):
    """Converts object into dictionary"""
    if not hasattr(obj, "__dict__"):
        return obj
    result = {}
    for key, value in obj.__dict__.items():
        if key.startswith("_"):
            continue
        element = []
        if isinstance(value, list):
            for item in value:
                element.append(my_dict(item))
        else:
            element = my_dict(value)
        result[key] = element
    return result


def pi(n):
    """Calculates n digits of pi using the spigot algorithm"""
    l = list()
    k, a, b, a1, b1 = 2, 4, 1, 12, 4
    while n > 0:
        p, q, k = k * k, 2 * k + 1, k + 1
        a, b, a1, b1 = a1, b1, p * a + q * a1, p * b + q * b1
        d, d1 = a / b, a1 / b1
        while d == d1 and n > 0:
            l.append(int(d))
            n -= 1
            a, a1 = 10 * (a % b), 10 * (a1 % b1)
            d, d1 = a / b, a1 / b1
    return l


def pi_float(n):
    """Returns float value of spigot algorithm"""
    l = pi(n)
    f = "3."
    for i in range(1, n):
        f += str(l[i])
    return float(f)


def remap(v, l1, h1, l2, h2):
    """Re-maps a number from one range to another"""
    return float(v - l1) / (h1 - l1) * (h2 - l2) + l2


def shuffled(l):
    """Returns shuffled list"""
    result = l[:]
    shuffle(result)
    return result
