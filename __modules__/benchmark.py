from time import clock


def benchmark(f, a, n, calibrate=False):
    """Benchmarks a function"""
    print("##### {0} #####".format(f.__name__))
    r = range(n)
    offset = 0
    if calibrate:  # Minimize function call overhead
        def e(): pass
        t1 = clock()
        for i in r:  # Minimize loop overhead
            e(); e(); e(); e(); e(); e(); e(); e(); e(); e()
        t2 = clock()
        offset = t2 - t1
    t1 = clock()
    for i in r:  # Minimize loop overhead
        f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a)
    t2 = clock()
    time = round(t2 - t1 - offset, 5)
    print("total time:", time)
    print("loop time:", round(time / (10 * n), 5))
    return time


def compare(f1, f2, a1, a2, n, calibrate=False):
    """Compares two functions"""
    t1 = benchmark(f1, a1, n, calibrate=calibrate)
    t2 = benchmark(f2, a2, n, calibrate=calibrate)

    if t1 / t2 < 1:
        print("{0} is {2}% faster than {1}".format(f1.__name__, f2.__name__, round((1 - t1 / t2) * 100, 2)))
    elif t2 / t1 < 1:
        print("{0} is {2}% faster than {1}".format(f2.__name__, f1.__name__, round((1 - t2 / t1) * 100, 2)))
    else:
        print("{0} and {1} perform exactly the same".format(f1.__name__, f2.__name__))
