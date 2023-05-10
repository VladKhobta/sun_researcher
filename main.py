from functions import start_simulation
from models import Sun, SolarPanel
from functions.plots import show_plot
from pprint import pprint
import matplotlib.pyplot as plt
from datetime import date
from functions.calculations import *
from nasa import get_data
from math import floor, ceil

LATITUDE = 55.74
LONGITUDE = 37.63
GMT_DELTA = 3
DISCRETENESS = 240
STEP = 1

DATE = date(2022, 5, 5)
DAYS = DATE.timetuple().tm_yday

START = 5.1
END = 23

B = calc_b_coefficient(DAYS)
DECLINATION = calc_declination_angle(B)


if __name__ == '__main__':
    # initializing objects
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

    # start simulation
    data = start_simulation(
        sun,
        panel,
        get_data(LONGITUDE, LATITUDE, DATE),
        START,
        END,
    )

    show_plot(*data[:-2])
    summary_irradiation = sum(data[-2])

    print(summary_irradiation)

    # pprint(data[-1])
    # pprint(data[-2])
    plt.plot(list(range(floor(START), ceil(END) - 1)), data[-2])
    plt.show()
