from math import pi, cos, sin, asin, acos, degrees, radians


def equation_of_time(n):
    b = 2 * pi * (n - 81) / 365
    e = 7.53 * cos(b) + 1.5 * sin(b) - 9.87 * sin(2 * b)

    return -e


def sun_angles(d, lt, delta_gtm, longitude, latitude):
    lstm = 15 * delta_gtm
    tc = 4 * (longitude - lstm) + equation_of_time(d)
    lst = lt + tc / 60
    hra = radians(15 * (lst - 12))
    delta = radians(23.45 * sin(radians((360 / 365) * (d - 81))))

    elevation = degrees(asin(
        sin(delta) * sin(latitude) + cos(delta) * cos(latitude) * cos(hra)
    ))
    azimuth = degrees(
        acos((
                sin(delta) * cos(latitude) - cos(delta) * sin(latitude) * cos(hra) /
                cos(radians(elevation))
        ))
    )
    return 90 - elevation, azimuth


if __name__ == '__main__':
    for i in range(12):
        print(equation_of_time(i))

    print(equation_of_time(4.5 * 30))
    print(sun_angles(121, 16.25, 3, radians(37), radians(55)))
