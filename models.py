from functions import sun_position
from math import sin, cos, radians, degrees, pi, asin, acos


class Sun:
    def __init__(self, longitude, latitude, gtm_delta):
        self.azimuth_angle = None
        self.elevation_angle = None
        self.second_part = False
        self.gtm_delta = gtm_delta
        self.longitude = radians(longitude)
        self.latitude = radians(latitude)


    def update_position(self, days, hours):
        self.elevation_angle, self.azimuth_angle = [
            degrees(a) for a in self.get_current_position(days, hours)
        ]

    def get_current_position(self, days, hours):
        lstm = 15 * self.gtm_delta
        b = self.get_b_coefficient(days)
        equation_of_time = 9.87 * sin(2 * b) - 7.53 * cos(b) - 1.5 * sin(b)
        time_correction = 4 * (degrees(self.longitude) - lstm) + equation_of_time  # minutes
        local_solar_time = hours + time_correction / 60
        hra = radians(15 * (local_solar_time - 12))

        declination = self.get_declination_angle(b)

        elevation = asin(
            sin(declination) * sin(self.latitude) +
            cos(declination) * cos(self.latitude) * cos(hra)
        )

        azimuth = acos(
            (
                sin(declination) * cos(self.latitude) -
                cos(declination) * sin(self.latitude) * cos(hra)
            ) / cos(elevation)
        )

        return elevation, azimuth


    @staticmethod
    def get_declination_angle(b):
        return radians(23.45 * sin(b))


    @staticmethod
    def get_b_coefficient(days):
        return radians(360 / 365 * (days - 81))



class SolarPanel:
    def __init__(self):
        self.azimuth_angle = 0  # 0 -- north, clockwise
        self.elevation_angle = 90
        pass

    def change_angle(self, sun_azimuth, sun_elevation):
        self.azimuth_angle = sun_azimuth
        self.elevation_angle = sun_elevation


if __name__ == '__main__':
    sun = Sun(37.63, 55.74, 3)

    for i in range(4, 18):
        sun.update_position(119, i)
        print(sun.elevation_angle, sun.azimuth_angle)
        # print(sun_position(119, i, 3, 37.63, 55.74))
