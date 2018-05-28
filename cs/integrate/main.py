import chart
import integrate
import math

if __name__ == "__main__":
    # Define variables
    # f = function
    # i = interval
    # n = trapez count
    # e = epsilon
    f = lambda x: math.e ** (-(x - 2)**2 / 0.05) + math.e**(-(x - 5)**2 / 0.1) + 0.1 * x - math.e**(-(x - 3.5)**2 / 0.1)
    i = (1, 7)
    n = 10
    e = 0.001

    # Draw function, save it under "graphics/function.svg"
    # Use 1000 data points to get a smooth graph
    chart.draw(f, i[0], i[1], 1000)
    chart.save("Graph", "graphics/graph.svg")
    chart.reset()

    # Calculate the interval using trapezoidal integration
    trapez_res = integrate.trapezoidal(f, i[0], i[1], 10)
    print("Trapezoidal integration result =", trapez_res)

    # Calculate the integral using adaptive integration
    adaptive_res, adaptive_n = integrate.adaptive(f, i[0], i[1], n, e)
    print("Adaptive integration result =", adaptive_res, "using n =", adaptive_n)

    # Draw a chart comparing the two
    chart.draw(f, i[0], i[1], 10, dots=True, graph_name="trapezoidal", dots_name="trapezoidal interval borders")
    chart.draw(f, i[0], i[1], adaptive_n, dots=True, graph_name="adaptive", dots_name="adaptive interval borders")
    chart.save("Comparison", "graphics/comparison.svg")
    chart.reset()
