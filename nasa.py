from math import floor, ceil
from datetime import date, datetime, time
from pprint import pprint
import requests
from matplotlib import pyplot as plt

API = 'https://power.larc.nasa.gov/api/temporal'


def get_data(
        longitude: float,
        latitude: float,
        utc_date: date,
):
    start = end = utc_date.strftime("%Y%m%d")

    response = requests.get(
        API + f'/hourly/point?'
              f'start={start}'
              f'&end={end}'
              f'&latitude={latitude}'
              f'&longitude={longitude}'
              f'&community=RE'
              f'&parameters=ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,ALLSKY_KT,ALLSKY_SRF_ALB,SZA'
              f'&user=DAVEDownload'
              f'&format=json'
    )
    data = response.json()
    return parse(data['properties']['parameter'])


def parse(data):
    new_data = {}
    for parameter in data:
        new_data[parameter] = {}
        for key in data[parameter]:
            new_data[parameter][key[8:]] = data[parameter][key]

    return new_data


if __name__ == '__main__':
    longitude_ = 37.63
    latitude_ = 55.74
    data = get_data(longitude_, latitude_, date(2022, 6, 5))

    time = list(range(0, 24))
    pprint(time)

    for parameter in data:
        plt.plot(time, data[parameter].values())
        plt.show()
