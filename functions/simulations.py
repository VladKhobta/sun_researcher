from math import degrees, floor
from pprint import pprint
from models import Sun, SolarPanel
from functions.calculations import *


def time_goes(start, end, step):
    def time_goes_decorator(simulation):
        def wrapper(*args, **kwargs):
            sun_positions = []
            panel_positions = []
            radiances = []

            for i in range(
                    round(start * 60),
                    round(end * 60) + 1,
                    step
            ):
                sun_position, panel_position, radiance = simulation(*args, i, **kwargs)
                sun_positions.append(sun_position)
                panel_positions.append(panel_position)
                radiances.append(radiance)

            return sun_positions, panel_positions, radiances

        return wrapper

    return time_goes_decorator


@time_goes(10, 12, 1)
def simulate_tracking(sun, panel, minute):
    panel.send(10)
    panel = next(panel)
    return minute, next(sun), panel


class Panel:
    def __init__(self, longitude, latitude, gtm_delta, days, minute, discreteness, static):
        # CONSTS
        # days-based
        self.b = calc_b_coefficient(days)
        self.declination = calc_declination_angle(self.b)

        # from args
        self.longitude = radians(longitude)
        self.latitude = radians(latitude)
        self.gtm_delta = gtm_delta
        self.discreteness = discreteness
        self.days = days
        self.static = static
        self.minute = minute

        self.beta = pi / 2
        self.position = (0, 0)

    def __next__(self):
        returning = self.position
        sun_position = calc_solar_position(
            self.longitude,
            self.latitude,
            self.gtm_delta,
            self.declination,
            self.minute / 60,
            self.b
        )
        if not self.minute % self.discreteness:
            self.position = sun_position

        hra = calc_hra(self.longitude, self.gtm_delta, self.minute / 60, self.b)
        theta_z = calc_theta_z_angle(
            self.latitude,
            self.declination,
            hra,
        )
        theta = calc_theta_angle(
            theta_z,
            self.beta
        )

        self.insolation = calc_radiation(
            self.beta,
            all_sky_irradiance,
            k_t,
            theta_z,
            theta,
            albedo
        )

        self.minute += 1
        return returning

    def __iter__(self):
        return self


class Sunn:
    def __init__(self, longitude, latitude, gtm_delta, days, minute):
        self.b = calc_b_coefficient(days)
        self.declination = calc_declination_angle(self.b)

        self.longitude = radians(longitude)
        self.latitude = radians(latitude)

        self.gtm_delta = gtm_delta

        self.position = (0, 0)
        self.minute = minute

    def get_current_position(self):
        return calc_solar_position(
            self.longitude,
            self.latitude,
            self.gtm_delta,
            self.declination,
            self.minute,
            self.b
        )

    def __next__(self):
        current_position = self.position
        self.minute += 1
        self.position = self.get_current_position()
        return current_position

    def __iter__(self):
        return self


if __name__ == '__main__':
    sun_ = Sunn(55.74, 37.63, 3, 119, 10 * 60)
    panel_ = Panel()
    pprint(simulate_tracking(sun_, panel_))


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
