"""
This is a simple script to find intersections points in a given range.
Instructions:
    Call the function plotIntersection with these arguments:
    - numbers: A linear space of numbers.
    - f, g: Functions.

Author: Avshalom Avraham
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


def plotIntersection(numbers, f, g):
    # Plot the 2 functions:
    plt.plot(numbers, f(numbers))
    plt.plot(numbers, g(numbers))

    # Try fsolve with multiple points from 'numbers' space.
    # If a point was found in 'numbers' range - plot a red circle on that point.
    for i in numbers:
        [point, info, found, err] = fsolve(lambda x: f(x) - g(x), x0=i, full_output=True)
        if found and point <= max(numbers):
            plt.plot(point, f(point), 'ro')

    plt.show()


if __name__ == '__main__':
    # Test 1:
    x = np.linspace(-10, 10, 40)
    f = lambda x: np.sin(2*x)
    g = lambda x: x + 1
    plotIntersection(x, f, g)

    # Test 2:
    x = np.linspace(-5, 25, 50)
    f = lambda x: x**2
    g = lambda x: 2*x
    plotIntersection(x, f, g)

    # Test 3:
    x = np.linspace(-10, 20, 20)
    f = lambda x: np.cos(x)
    g = lambda x: x+3
    plotIntersection(x, f, g)

    # Test 4:
    x = np.linspace(-20, 20, 30)
    f = lambda x: x**3
    g = lambda x: x+5
    plotIntersection(x, f, g)
