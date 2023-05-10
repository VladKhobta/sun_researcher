from math import sin, cos, radians, degrees, asin, acos, sqrt, copysign, pi


def calc_theta_z_angle(latitude, declination, hra):
    return acos(
        cos(latitude) * cos(declination) * cos(hra)
        + sin(latitude) * sin(declination)
    )


def calc_theta_angle(theta_z, beta, gamma_solar, gamma_surface):
    # print(theta_z, beta, gamma_solar, gamma_surface)
    # print('rounded')
    # print(round(cos(theta_z) * cos(beta) + sin(theta_z) * sin(beta) * cos(gamma_solar - gamma_surface), 4))

    return acos(
        round(cos(theta_z) * cos(beta) + sin(theta_z) * sin(beta) * cos(gamma_solar - gamma_surface), 4)
    )


def calc_declination_angle(b):
    return radians(23.45 * sin(b))


def calc_b_coefficient(days):
    return radians(360 / 365 * (days - 81))


def calc_hra(longitude, gtm_delta, hour, b, ):
    lstm = 15 * gtm_delta
    equation_of_time = 9.87 * sin(2 * b) - 7.53 * cos(b) - 1.5 * sin(b)
    time_correction = 4 * (degrees(longitude) - lstm) + equation_of_time  # minutes
    local_solar_time = hour + time_correction / 60
    hra = radians(15 * (local_solar_time - 12))
    return hra


def calc_azimuth_angle(latitude, declination, theta_z, hra):
    return copysign(1, hra) * abs(
        acos(
            (cos(theta_z) * sin(latitude) - sin(declination)) /
            (sin(theta_z) * cos(latitude))
        )
    )


def calc_directed_to_whole_ratio(k_t):
    if k_t <= 0.22:
        return 1 - 0.09 * k_t
    if k_t > 0.8:
        return 0.165
    return 0.9511 - 0.1604 * k_t + 4.388 * (k_t ** 2) - 16.638 * (k_t ** 3) + 12.336 * (k_t ** 4)


def calc_radiation(beta, all_sky_downward_irradiance, k_t, theta_z, theta, ro):

    d_w_ratio = calc_directed_to_whole_ratio(k_t)
    flat_directed_irradiation = (1 - d_w_ratio) * all_sky_downward_irradiance
    flat_diffused_irradiation = d_w_ratio * all_sky_downward_irradiance

    directed_irradiation = flat_directed_irradiation * cos(theta) / cos(theta_z)
    diffused_irradiation = flat_diffused_irradiation * (1 + cos(beta)) / 2
    reflected_irradiation = ro * all_sky_downward_irradiance * (1 - cos(beta)) / 2

    insolation = directed_irradiation + diffused_irradiation + reflected_irradiation

    return insolation

