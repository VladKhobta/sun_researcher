from functions import tracking_simulation
from models import Sun, SolarPanel
from functions.plots import show_plot
from pprint import pprint
import matplotlib.pyplot as plt
# from datetime import date
# from functions.calculations import *
from nasa import get_data
from math import floor, ceil
from configuration import *


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
        DISCRETENESS,
        True
    )
    panel.position = (
        0, 0
    )
    panel.beta = pi

    # start simulation
    data = tracking_simulation(
        sun,
        panel,
        get_data(LONGITUDE, LATITUDE, DATE),
        START,
        END,
    )

    show_plot(
        *data[:-2],
        data[-2],
        list(range(floor(START), ceil(END) - 1))
    )
    summary_irradiation = sum(data[-2])

    print(summary_irradiation)

    # pprint(data[-1])
    # pprint(data[-2])
    # plt.plot(list(range(floor(START), ceil(END) - 1)), data[-2])
    # plt.show()
