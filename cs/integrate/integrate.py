def trapezoidal(f, a, b, n):
    """
    Integrates a function within an interval.

    Source: https://stackoverflow.com/a/21146650/7057528

    :param f: function
    :param a: interval left
    :param b: interval right
    :param n: trapez count
    :return: integral
    """
    step = abs(b - a) / n
    s = f(a) / 2
    for i in range(1, n):
        s += f(a + i * step)
    s += f(b) / 2
    return s * step


def adaptive(f, a, b, n, eps):
    """
    Integrates a function within an interval. Might result in an infinity loop if epsilon is unreachable.

    Source: http://hplgit.github.io/prog4comp/doc/pub/._p4c-bootstrap-Python018.html

    :param f: function
    :param a: interval left
    :param b: interval right
    :param n: trapez count
    :param eps: epsilon
    :return: (integral, n)
    """
    i_n1 = trapezoidal(f, a, b, n)
    i_n2 = trapezoidal(f, a, b, n + 1)
    n += 1
    while abs(i_n2 - i_n1) > eps:
        i_n1 = trapezoidal(f, a, b, n)
        i_n2 = trapezoidal(f, a, b, n + 1)
        n += 1
    return i_n2, n