import time


def benchmark(n, end="\n"):
    """
    Decorator used to benchmark a function.

    :param n: amount of repeats
    :param end: suffix for last print
    :returns: total time
    """
    def decorate(func):
        """
        Main decorator.

        :param func: function to benchmark
        :returns: total time
        """
        def wrap(*args, **kwargs):
            """
            Wraps around the function.

            :param args: arguments
            :param kwargs: keyword arguments
            :returns: total time
            """
            print("########## {} ##########".format(func.__name__))
            start = time.time()
            for _ in range(n):
                func(*args)
            total = (time.time() - start) * 1000.0
            print("total time for {} loops: {:.3f} ms".format(n, total))
            print("average time for each loop: {:.3f} ms".format(total / n), end=end)
            return total

        return wrap

    return decorate


def compare(fun1, res1, fun2, res2):
    """
    Compares two benchmark results.

    :param fun1, fun2: names
    :param res1, res2: results
    :returns: None
    """
    res = res1 / res2
    if res > 1:
        fun1, fun2 = fun2, fun1
    else:
        res = 1 / res
    print("{} is {:.2f}x faster than {}".format(fun1, res, fun2))


def versus(fun1, fun2, n, args=()):
    """
    Complete benchmark for two functions.

    :param fun1, fun2: functions
    :param n: amount of repeats
    :param args: arguments
    :returns: None
    """
    args = args if isinstance(args, tuple) else (args,)
    dec1 = benchmark(n, end="\n\n")(fun1)
    dec2 = benchmark(n, end="\n\n")(fun2)
    res1 = dec1(*args)
    res2 = dec2(*args)
    compare(fun1.__name__, res1, fun2.__name__, res2)
