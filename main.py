import time
from pprint import pprint
from models import Sun, SolarPanel
from functions import show_plot


START_HOUR = 6
END_HOUR = 18
START_TIME = START_HOUR * 60
END_TIME = END_HOUR * 60
WORK_INTERVAL = END_TIME - START_TIME

DISCRETENESS = 60  # minutes

DAYS_OF_YEAR = 360
LONGITUDE = 37.63
LATITUDE = 55.74

GREENWICH_TIME_DELTA = 3


if __name__ == '__main__':
    sun_position_data = []
    solar_panel_position_data = []
    time_data = []

    solar_panel = SolarPanel()
    sun = Sun(LONGITUDE, LATITUDE, GREENWICH_TIME_DELTA)

    sun.update_position(DAYS_OF_YEAR, START_TIME / 60)
    solar_panel.change_angle(sun.azimuth_angle, sun.elevation_angle)
    for i in range(START_TIME, END_TIME, 1):
        # print(f'Now is {i / 60} hours')
        # sun position is updating
        previous_azimuth = sun.azimuth_angle
        sun.update_position(DAYS_OF_YEAR, i / 60)

        if previous_azimuth > sun.azimuth_angle:
            print('Add')
            sun.second_part = True
            sun.update_position(DAYS_OF_YEAR, i / 60)

        if not i % DISCRETENESS:
            solar_panel.change_angle(sun.azimuth_angle, sun.elevation_angle)

        # print(f'Sun position: {sun.elevation_angle, sun.azimuth_angle}')
        # print(f'Solar panel angles: {solar_panel.elevation_angle, solar_panel.azimuth_angle}')
        solar_panel_position_data.append([solar_panel.elevation_angle, solar_panel.azimuth_angle])
        sun_position_data.append([sun.elevation_angle, sun.azimuth_angle])
        time_data.append(i / 60)
        time.sleep(0)

    show_plot(time_data, sun_position_data, solar_panel_position_data)
