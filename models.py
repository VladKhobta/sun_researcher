from functions.calculations import *


class Sun:
    def __init__(self, longitude, latitude, gtm_delta, days):
        # CONSTS
        # calculated
        self.b = calc_b_coefficient(days)
        self.declination = calc_declination_angle(self.b)

        # from args
        self.longitude = radians(longitude)
        self.latitude = radians(latitude)
        self.days = days
        self.gtm_delta = gtm_delta

        # initializing
        self.position = ()  # elevation, azimuth

    def update(self, hours):
        self.position = self.get_current_position(hours)

    def get_current_position(self, hour):
        return calc_solar_position(
            self.longitude,
            self.latitude,
            self.gtm_delta,
            self.declination,
            hour,
            self.b
        )


class SolarPanel:
    def __init__(self, longitude, latitude, gtm_delta, days, discreteness=30, static=False):
        # CONSTS
        # days-based
        self.b = calc_b_coefficient(days)
        self.declination = calc_declination_angle(self.b)

        # from args
        self.latitude = radians(latitude)
        self.longitude = radians(longitude)
        self.gtm_delta = gtm_delta
        self.discreteness = discreteness
        self.days = days
        self.static = static

        # initializing
        self.position = (
            pi / 8,
            - pi / 2
        )  # 0 azimuth -- south, clockwise
        if self.static:
            self.position = (
                pi / 4,
                0
            )
        self.theta = 0
        self.theta_z = 0
        self.beta = pi / 2 - self.position[0]

    def update(self, sun_elevation, sun_azimuth, hour):
        if not hour * 60 % self.discreteness and not self.static:
            self.position = (sun_elevation, sun_azimuth)
            self.beta = pi / 2 - self.position[0]

        hra = calc_hra(self.longitude, self.gtm_delta, hour, self.b)
        self.theta_z = calc_theta_z_angle(
            self.latitude,
            self.declination,
            hra
        )
        self.theta = calc_theta_angle(
            self.theta_z,
            self.beta,
            sun_azimuth,
            self.position[1]
        )

    def calc_insolation(self, all_sky_irradiance, k_t, albedo):
        all_sky_irradiance *= 0.0036
        # print(
        #     all_sky_irradiance,
        #     k_t,
        #     albedo
        # )
        if k_t < 0 or albedo < 0:
            return 0
        rad = calc_radiation(
            self.beta,
            all_sky_irradiance,
            k_t,
            self.theta_z,
            self.theta,
            albedo
        )
        print('Irradiation:', rad)
        return rad


if __name__ == '__main__':
    print(calc_radiation(radians(60), 1.04, 0.445, 1.0859, 0.64507, 0.6))
    print(radians(60))
    print(calc_theta_angle(1.066, 1.066, -1.2557, -1.2557))
    print(calc_radiation(0.946, 1.04, 0.445, 0.946, 0, 0.6))
