def trapezoidal_unoptimized(f, a, b, n):
    """
    Unoptimierte Variante der Trapezregel. Integriert eine Funktion mit Hilfe
    der Trapezregel im Interval [a, b].

    :param f: Funktion
    :param a: linke Intervallgrenze
    :param b: rechte Intervallgrenze
    :param n: Anzahl der betrachteten Trapeze
    :return: Integral im Intervall [a, b]
    """
    # Schrittlänge für Intervalle berechnen
    step = abs(b - a) / n
    # Variable s = Summe der Trapezflächen
    s = 0
    # Über alle Trapeze iterieren und deren Fläche aufsummieren
    for i in range(1, n + 1):
        s += ((f(a + i * step) + f(a + (i - 1) * step)) / 2) * step
    return s


def trapezoidal(f, a, b, n):
    """
    Optimierte Variante der Trapezregel. Integriert eine Funktion mit Hilfe der
    Trapezregel im Interval [a, b].

    :param f: Funktion
    :param a: linke Intervallgrenze
    :param b: rechte Intervallgrenze
    :param n: Anzahl der betrachteten Trapeze
    :return: Integral im Intervall [a, b]
    """
    # Schrittlänge für Intervalle berechnen
    step = abs(b - a) / n
    # Variable s = Summe der Trapezhöhen (y-Werte)
    # Die Funktionswerte der linken und rechten Intervallgrenze gehen nur zur
    # Hälfte in das Integral ein, da sie nur einmal vorkommen
    s = (f(a) + f(b)) / 2
    # Über alle Trapezhöhen iterieren und zur Summe addieren
    # Dies kann so gemacht werden, da alle diese Kanten von zwei Trapezen
    # geteilt werden
    for i in range(1, n):
        s += f(a + i * step)
    # Summe der Trapezhöhen mit der Schrittlänge multiplizieren um die Fläche,
    # also das Integral, zu erhalten
    return s * step


def adaptive(f, a, b, n, e):
    """
    Integriert eine Funktion im Interval [a, b]. Dafür wird die vorher
    definierte Trapezregel verwendet. Die Anzahl der betrachteten Trapeze wird
    so lange erhöht, bis der Unterschied des Integrals bei Erhöhung kleiner ist
    als der Fehler Epsilon.

    :param f: Funktion
    :param a: linke Intervallgrenze
    :param b: rechte Intervallgrenze
    :param n: Anzahl der betrachteten Trapeze
    :param e: Epsilon
    :return: (Integral, n)
    """
    # Integral für das übergebene n berechnen
    i1 = trapezoidal(f, a, b, n)
    # Integral für das nächsthöhere n berechnen
    n += 1
    i2 = trapezoidal(f, a, b, n)
    # Während die Differenz größer ist als der Fehler wird...
    while abs(i2 - i1) > e:
        # ... das alte Integral zwischengespeichert...
        i1 = i2
        # ... und das neues Integral für das nächsthöhere n berechnet
        n += 1
        i2 = trapezoidal(f, a, b, n)
    # Zurückgegeben werden das Integral und die Anzahl der betrachteten Trapeze,
    # da diese zum Zeichnen der Funktion genötigt wird
    return i2, n
