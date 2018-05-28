import leather

_chart = leather.Chart()
_count = 0
_colors = [("#FF0000", "#FFA500"), ("#0000FF", "#800080")]


def reset():
    """
    Resets the current chart.

    :return: None
    """
    global _chart, _count
    _chart = leather.Chart()
    _count = 0


def draw(f, a, b, n, graph=True, dots=False, dots_name="", graph_name=""):
    """
    Draws a function.

    :param f: function
    :param a: interval left
    :param b: interval right
    :param n: data points
    :param graph: show graph, default true
    :param dots: show dots, default false
    :param dots_name: dot name
    :param graph_name: graph name
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
    Saves a function as svg.

    :param title: title
    :param path: path
    :return: None
    """
    global _chart
    _chart._title = title
    _chart.to_svg(path)