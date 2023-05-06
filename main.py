from functions.simulations import start_simulation
from models import Sun, SolarPanel
from functions.plots import show_plot
from pprint import pprint
import matplotlib.pyplot as plt
from datetime import date
from functions.calculations import *

LATITUDE = 55.74
LONGITUDE = 37.63
GMT_DELTA = 3
DISCRETENESS = 200
STEP = 1

DATE = date(2022, 6, 5)
DAYS = DATE.timetuple().tm_yday

START = 8
END = 16

B = calc_b_coefficient(DAYS)
DECLINATION = calc_declination_angle(B)


if __name__ == '__main__':
    sun = Sun(
        LONGITUDE,
        LATITUDE,
        GMT_DELTA,
        DAYS
    )
    panel = SolarPanel(
        LONGITUDE,
        LATITUDE,
        GMT_DELTA,
        DAYS,
        DISCRETENESS
    )
    data = start_simulation(sun, panel, 8, 16, STEP)

    pprint(data[2][:10])
    pprint(data[1][:10])
    print(len(data[2]))
    show_plot(*data[:-1])

    summary_irradiation = sum(map(lambda x: x * STEP / 60, data[-1]))

    print(summary_irradiation)

    plt.plot(data[0], data[-1])
    plt.show()
