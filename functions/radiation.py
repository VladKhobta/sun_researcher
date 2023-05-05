from math import cos, sin
import requests
from pprint import pprint

API = 'https://power.larc.nasa.gov'


def calculate_radiation(beta, gamma, delta, phi, omega):

    ro = 0.367

    # i_direct = i_flat_direct * cos(theta_z) / theta
    # i_scattered = i_flat_scattered * (1 + cos(beta)) / 2
    # i_reflected = ro * i_flat_reflected * (1 - cos(beta)) / 2

    # insolation = i_direct + i_scattered + i_reflected


if __name__ == '__main__':
    response = requests.get(API + '/api/application/indicators/point?longitude=-84.43&latitude=33.64&start=2015&end=2021&format=JSON')
    pprint(response.json())
