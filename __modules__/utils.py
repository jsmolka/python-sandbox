from random import shuffle


def create_class(name, arg_names):
    """Creates class dynamically"""
    class BaseClass(object):
        def __init__(self):
            pass

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in arg_names:
                raise TypeError("Argument %s not valid for %s"
                    % (key, self.__class__.__name__))
            setattr(self, key, value)

    return type(name, (BaseClass,),{"__init__": __init__})


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
