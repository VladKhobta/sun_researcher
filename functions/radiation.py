from math import cos, sin, radians, sqrt, copysign, acos
import requests
from pprint import pprint
from functions.calculations import *

API = 'https://power.larc.nasa.gov'


def calculate_radiation(beta, all_sky_downward_irradiance, k_t, theta_z, theta, ro):

    d_w_ratio = calc_directed_to_whole_ratio(k_t)
    flat_directed_irradiation = (1 - d_w_ratio) * all_sky_downward_irradiance
    flat_diffused_irradiation = d_w_ratio * all_sky_downward_irradiance

    directed_irradiation = flat_directed_irradiation * cos(theta) / cos(theta_z)
    diffused_irradiation = flat_diffused_irradiation * (1 + cos(beta)) / 2
    reflected_irradiation = ro * all_sky_downward_irradiance * (1 - cos(beta)) / 2

    insolation = directed_irradiation + diffused_irradiation + reflected_irradiation

    return insolation


def kek(latitude, declination, hra):
    azimuth = copysign(1, hra) * abs(
        acos(
            (cos(theta_z) * sin(latitude) - sin(declination)) /
            (sin(theta_z) * cos(latitude))
        )
    )
    return azimuth


if __name__ == '__main__':
    # response = requests.get(
    #     API + '/api/application/indicators/point?longitude=-84.43&latitude=33.64&start=2015&end=2021&format=JSON')
    # pprint(response.json())
    #
    print(calc_directed_to_whole_ratio(0.445))
    theta_z = calc_theta_z_angle(radians(40), radians(-11.6), radians(-37.5))
    print('angles')
    print(theta_z)
    theta = calc_theta_angle(theta_z, radians(60), kek(radians(40), radians(-11.6), radians(-37.5)), 0)
    print(theta)

    print(calculate_radiation(radians(60), 1.04, 0.445, theta_z, theta, 0.6))
