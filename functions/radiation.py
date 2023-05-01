from math import cos, sin


def calculate_radiation(beta, gamma, delta, phi, omega):

    cos_theta = sin(delta) * sin(phi) * cos(beta)
    - sin(delta) * cos(phi) * sin(beta) * cos(gamma)
    + cos(delta) * cos(phi) * cos(beta) * cos(omega)
    + cos(delta) * sin(phi) * sin(beta) * cos(gamma) * cos(omega)
    + cos(delta) * sin(beta) * sin(gamma) * sin(omega)



    return cos_theta
