from models import Sun, SolarPanel
from math import degrees


def start_simulation(sun: Sun, panel: SolarPanel, start, end, step=1) -> ():
    sun_data = []
    panel_data = []
    time_data = []
    radiation_data = []
    for minute in range(start * 60, end * 60, step):
        current_hour = minute / 60

        # updating positions
        sun.update(current_hour)
        panel.update(*sun.position, current_hour)

        # collecting data
        sun_data.append((*map(degrees, sun.position), ))
        panel_data.append((*map(degrees, panel.position), ))
        time_data.append(minute / 60)
        radiation_data.append(panel.calc_insolation())

        # output
        if not minute % 30:
            print(
                f'Hour: {current_hour}\n'
                f'Beta: {panel.beta}\n'
                f'Theta_z: {panel.theta_z}\n'
                f'Theta: {panel.theta}\n'
                f'Sun: {(*sun.position, )}\n'
                f'Panel: {panel.elevation_angle, degrees(panel.azimuth_angle)}\n'
                f'Radiation: {panel.calc_insolation()}\n'
                )

    return time_data, sun_data, panel_data, radiation_data
