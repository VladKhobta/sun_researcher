from math import degrees, floor

from models import Sun, SolarPanel


def tracking_simulation(
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


def static_simulation(
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

    k_t_data = []
    down_irrad_data = []
    albedo_data = []

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
        k_t_data.append(nasa_data['All Sky Surface Shortwave Downward Irradiance'][str(current_hour).zfill(2)])
        down_irrad_data.append(nasa_data['All Sky Insolation Clearness Index'][str(current_hour).zfill(2)])
        albedo_data.append(nasa_data['All Sky Surface Albedo'][str(current_hour).zfill(2)])

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
