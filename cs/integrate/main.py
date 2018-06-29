import chart
import integrate
import math

if __name__ == "__main__":
    # Benötigte Variablen definieren
    # 1. f = Funktion
    # 2. i = Interval [a, b]
    # n = Anzahl der betrachteten Trapeze
    # e = Epsilon
    f = lambda x: math.e**(-(x - 2)**2 / 0.05) + math.e**(-(x - 5)**2 / 0.1) + 0.1 * x - math.e**(-(x - 3.5)**2 / 0.1)
    i = (1, 7)
    n = 10
    e = 0.001

    # 3. Funktion darstellen, wird unter "graphics/function.svg" gespeichert
    # Die Anzahl der verwendeten Datenpunkte wird auf 1000 gesetzt, damit eine
    # ausreichend genaue Funktion entsteht
    chart.draw(f, i[0], i[1], 1000)
    chart.save("Graph", "graphics/graph.svg")
    chart.reset()

    # 5. Das Integral der Funktion f im Interval [a, b] mit n = 10 gleichgroßen
    # Teilintervallen berechnen
    trapez_int = integrate.trapezoidal(f, i[0], i[1], 10)
    print("Integral Trapezregel (optimiert):", round(trapez_int, 5))

    # Funktion darstellen, wird unter "graphics/trapezoidal.svg" gespeichert
    chart.draw(f, i[0], i[1], 10, dots=True, graph_name="Trapezregel", dots_name="Trapezkanten")
    chart.save("Trapezregel", "graphics/trapezoidal.svg")
    chart.reset()

    # Als Test den Wert der unoptimierten Funktion berechnen
    print("Integral Trapezregel (unoptimiert):", round(integrate.trapezoidal_unoptimized(f, i[0], i[1], 10), 5))

    # 6. Das Integral der Funktion f im Interval [a, b] mit n = 10 als Startwert
    # berechnen
    adaptive_int, adaptive_n = integrate.adaptive(f, i[0], i[1], n, e)
    print("Integral adaptive Integration:", round(adaptive_int, 5), "für n =", adaptive_n)

    # Funktion darstellen, wird unter "graphics/adaptive.svg" gespeichert
    chart.draw(f, i[0], i[1], adaptive_n, dots=True, graph_name="Adaptive Integration", dots_name="Trapezkanten")
    chart.save("Adaptive Integration", "graphics/adaptive.svg")
    chart.reset()

    # 7. Ergebnisse vergleichen
    l = "Trapezregel"
    r = "adaptiven Integration"
    if adaptive_int > trapez_int:
        l, r = r, l
    print("Das Ergebnis der {} ist größer als das der {}.".format(l, r))

    # 8. Zum vergleich der beiden verfahren werden deren Graphen für die Anzahl der
    # betrachteten Trapeze gezeichnet. Wird unter "graphics/comparison.svg"
    # gespeichert
    chart.draw(f, i[0], i[1], 10, dots=True, graph_name="Trapezregel", dots_name="Trapezregel Trapezkanten")
    chart.draw(f, i[0], i[1], adaptive_n, dots=True, graph_name="Adaptiv", dots_name="Adaptiv Trapezkanten")
    chart.save("Vergleich", "graphics/comparison.svg")
    chart.reset()

    input("\nZum Beenden Enter drücken...")
