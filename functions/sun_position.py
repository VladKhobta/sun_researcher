from math import sin, cos, asin, acos, degrees, radians, pi


def sun_position(days, hours, d_gtm, longitude, latitude, second_part=None):
    lstm = 15 * d_gtm
    b = radians(360 / 365 * (days - 81))
    eot = 9.87 * sin(2 * b) - 7.53 * cos(b) - 1.5 * sin(b)
    tc = 4 * (longitude - lstm) + eot
    lst = hours + tc / 60
    hra = radians(15 * (lst - 12))

    declination = radians(23.45 * sin(b))

    elevation = asin(
        sin(declination) * sin(radians(latitude)) +
        cos(declination) * cos(radians(latitude)) * cos(hra)
    )

    azimuth = acos(
        (sin(declination) * cos(radians(latitude)) - cos(declination) * sin(radians(latitude)) * cos(hra)) /
        cos(elevation)
    )

    return degrees(elevation), degrees(azimuth) if not second_part else 360 - degrees(azimuth)


if __name__ == '__main__':
    for i in range(6, 12):
        print(i, sun_position(121, i, 3, 37.63, 55.74))

