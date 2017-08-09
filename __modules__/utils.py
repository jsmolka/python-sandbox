def remap(value, low1, high1, low2, high2):
    """Re-maps a number from one range to another"""
    return float(value - low1) / (high1 - low1) * (high2 - low2) + low2

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

def int_to_rgb(v):
    """Converts int to rgb"""
    rgb = "{:024b}".format(v)
    return [int(rgb[:8], 2), int(rgb[8:16], 2), int(rgb[16:], 2)]

def rgb_to_int(v):
    """Converts rgb to int"""
    r = "{:08b}".format(v[0])
    g = "{:08b}".format(v[1])
    b = "{:08b}".format(v[2])
    return int(r + g + b, 2)
