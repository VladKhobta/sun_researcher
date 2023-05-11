from functions.calculations import *
from datetime import date

LATITUDE = 55.74
LONGITUDE = 37.63
GMT_DELTA = 3
DISCRETENESS = 1000
STEP = 1

DATE = date(2022, 6, 5)
DAYS = DATE.timetuple().tm_yday

START = 2
END = 23

B = calc_b_coefficient(DAYS)
DECLINATION = calc_declination_angle(B)
