import math
from math import sin, cos, asin, acos, pi


def calc(n, phi, theta, omega):

    delta = 23.45 * sin(2 * pi) * (284 + n) / 365
    alpha = asin(
        cos(phi) * cos(delta) * cos(omega) + sin(phi) * sin(delta)
    )

    gamma = sin(omega) * abs(acos(
        (cos(theta) * sin(phi) - sin(delta)) / (sin(theta) * cos(phi))
    ))

    return alpha, 2 * pi - gamma


if __name__ == '__main__':
    print([c * 180 / pi for c in calc(119, 37, 55, 15 * 60 * 60)])
    print(pi / 2 * 180 / pi)
