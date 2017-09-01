from time import clock


def benchmark(f, a, n, calibrate=False):
    """Benchmarks a function"""
    print("########## {0} ##########".format(f.__name__))
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
    raw_time = t2 - t1 - offset
    time = round(raw_time, 5)
    print("total time:", time)
    print("loop time:", round(raw_time / (10 * n), 5))
    return time


def compare(f1, f2, a1, a2, n, calibrate=False):
    """Compares two functions"""
    t1 = benchmark(f1, a1, n, calibrate=calibrate)
    t2 = benchmark(f2, a2, n, calibrate=calibrate)

    if t1 / t2 < 1:
        print("{0} is {2}x faster than {1}".format(f1.__name__, f2.__name__, round(1 / (t1 / t2), 2)))
    elif t2 / t1 < 1:
        print("{0} is {2}x faster than {1}".format(f2.__name__, f1.__name__, round(1 / (t2 / t1), 2)))
    else:
        print("{0} and {1} perform exactly the same".format(f1.__name__, f2.__name__))
