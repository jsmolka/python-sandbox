import leather

_chart = leather.Chart()
_count = 0
_colors = [("#FF0000", "#0000FF"), ("#006400", "#EE7600")]


def reset():
    """
    Setzt das momentane Diagramm zurück.

    :return: None
    """
    global _chart, _count
    _chart = leather.Chart()
    _count = 0


def draw(f, a, b, n, graph=True, dots=False, dots_name="", graph_name=""):
    """
    Zeichnet eine Funktion, indem für n-Werte im Interval [a, b] die y-Werte
    berechnet werden. Die Werte werden dann als Punkte dargestellt und mit einer
    Linie verbunden, welche den Graph darstellen soll.

    :param f: Funktion
    :param a: linke Intervallgrenze
    :param b: rechte Intervallgrenze
    :param n: Anzahl der Datenpunkte
    :param graph: Graph anzeigen, default True
    :param dots: Punkte anzeigen, default False
    :param dots_name: Legende für Punkte
    :param graph_name: Legende für Graphen
    :return: None
    """
    global _chart, _count
    step = abs(a - b) / n
    x = a
    data = []
    while x <= b:
        data.append((x, f(x)))
        x += step
    if graph:
        _chart.add_line(data, name=graph_name, stroke_color=_colors[_count][0])
    if dots:
        _chart.add_dots(data, name=dots_name, fill_color=_colors[_count][1])
    _count += 1


def save(title, path):
    """
    Speichert das momentane Diagram im angegebenen Pfad.

    :param title: Titel
    :param path: Speicherpfad
    :return: None
    """
    global _chart
    _chart._title = title
    _chart.to_svg(path)
