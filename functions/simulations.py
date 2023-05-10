from math import degrees, floor

from models import Sun, SolarPanel


def _start_simulation(sun: Sun, panel: SolarPanel, start, end, step, nasa_data) -> ():
    sun_data = []
    panel_data = []
    time_data = []
    radiation_data_averaged = []
    radiation_data_raw = {}

    sun.update(start)
    panel.update(*sun.position, 0)

    sum_insolation_measures = 0
    insolation_values_count = 0

    radiation_data_raw[floor(start)] = []
    for minute in range(floor(start * 60), floor(end * 60), step):
        current_hour = floor(minute / 60)
        if floor((minute - step) / 60) != current_hour:  # new hour starts. calculating new average insolation
            radiation_data_raw[current_hour] = []
            print(f'New Hour: {current_hour}\n')
            radiation_data_averaged.append(sum_insolation_measures / insolation_values_count)
            sum_insolation_measures = 0
            insolation_values_count = 0

        # updating positions
        sun.update(minute / 60)
        panel.update(*sun.position, minute / 60)

        # collecting data
        sun_data.append((*map(degrees, sun.position),))
        panel_data.append((*map(degrees, panel.position),))
        time_data.append(minute / 60)

        irradiation = panel.calc_insolation(
            nasa_data['All Sky Surface Shortwave Downward Irradiance'][str(current_hour).zfill(2)],
            nasa_data['All Sky Insolation Clearness Index'][str(current_hour).zfill(2)],
            nasa_data['All Sky Surface Albedo'][str(current_hour).zfill(2)]
        )

        sum_insolation_measures += irradiation
        insolation_values_count += 1
        radiation_data_raw[current_hour].append(irradiation)

        # output
        if not minute % 30:
            print(
                f'Hour: {current_hour}\n'
                f'Beta: {panel.beta}\n'
                f'Theta_z: {panel.theta_z}\n'
                f'Theta: {panel.theta}\n'
                f'Sun: {(*sun.position,)}\n'
                f'Panel: {(*panel.position,)}\n'
                f'Radiation: {irradiation}\n'
            )

    return time_data, sun_data, panel_data, radiation_data_averaged, radiation_data_raw


def start_simulation(
        sun: Sun,
        panel: SolarPanel,
        nasa_data: dict,
        start,
        end,
        step=1
):
    irradiation_data_raw = {}
    irradiation_data_averaged = []

    # data lists initializing
    time_data = []
    sun_data = []
    panel_data = []

    # initializing some values
    previous_hour = floor(round(start * 60) / 60)
    irradiation_data_raw[previous_hour] = []

    # starting main cycle
    for minute in range(
            round(start * 60),
            round(end * 60),
            step
    ):
        current_hour = floor(minute / 60)

        # handling new hour case
        if current_hour != previous_hour:  # new hour is starting
            irradiation_data_averaged.append(
                sum(irradiation_data_raw[previous_hour]) /
                len(irradiation_data_raw[previous_hour])
            )
            irradiation_data_raw[current_hour] = []
            previous_hour = current_hour

        # updating sun and panel states
        sun.update(minute / 60)
        panel.update(*sun.position, minute / 60)

        # calculating
        irradiation = panel.calc_insolation(
            nasa_data['All Sky Surface Shortwave Downward Irradiance'][str(current_hour).zfill(2)],
            nasa_data['All Sky Insolation Clearness Index'][str(current_hour).zfill(2)],
            nasa_data['All Sky Surface Albedo'][str(current_hour).zfill(2)]
        )

        # collecting data
        sun_data.append((*map(degrees, sun.position),))
        panel_data.append((*map(degrees, panel.position),))
        time_data.append(minute / 60)

        irradiation_data_raw[current_hour].append(irradiation)

        # output
        if not minute % 30:
            print(
                f'Hour: {current_hour}\n'
                f'Beta: {panel.beta}\n'
                f'Theta_z: {panel.theta_z}\n'
                f'Theta: {panel.theta}\n'
                f'Sun: {(*sun.position,)}\n'
                f'Panel: {(*panel.position,)}\n'
                f'Radiation: {irradiation}\n'
            )
            print(nasa_data['All Sky Surface Shortwave Downward Irradiance'][str(current_hour).zfill(2)],
                  nasa_data['All Sky Insolation Clearness Index'][str(current_hour).zfill(2)],
                  nasa_data['All Sky Surface Albedo'][str(current_hour).zfill(2)],
                  '\n'
                  )

    return time_data, sun_data, panel_data, irradiation_data_averaged, irradiation_data_raw
