from math import sin, cos, radians, degrees, asin, acos, sqrt, copysign, pi
from functions.calculations import *
from functions.plots import show_plot


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
        hra = calc_hra(self.longitude, self.gtm_delta, hour, self.b)

        theta_z = calc_theta_z_angle(self.latitude, self.declination, hra)
        azimuth = calc_azimuth_angle(self.latitude, self.declination, theta_z, hra)

        return pi / 2 - theta_z, azimuth


class SolarPanel:
    def __init__(self, longitude, latitude, gtm_delta, days, discreteness=30):
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

        # initializing
        self.azimuth_angle = 0  # 0 -- north, clockwise
        self.elevation_angle = 90
        self.theta = 0
        self.theta_z = 0
        self.beta = 0
        self.position = (pi / 2, 0)

    def update(self, sun_elevation, sun_azimuth, hour):
        if not hour * 60 % self.discreteness:
            self.azimuth_angle = sun_azimuth
            self.elevation_angle = sun_elevation
            self.beta = pi / 2 - sun_elevation
            self.position = (self.elevation_angle, self.azimuth_angle)

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
            self.azimuth_angle
        )

    def calc_insolation(self, ):
        return calc_radiation(self.beta, 1.04, 0.445, self.theta_z, self.theta, 0.6)


if __name__ == '__main__':
    print(calc_radiation(radians(60), 1.04, 0.445, 1.0859, 0.64507, 0.6))
    print(radians(60))
    print(calc_theta_angle(1.066, 1.066, -1.2557, -1.2557))
    print(calc_radiation(0.946, 1.04, 0.445, 0.946, 0, 0.6))
