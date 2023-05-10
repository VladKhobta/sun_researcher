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
    pprint(data)
    return parse(data['properties']['parameter'], data['parameters'])


def parse(data, parameters):
    new_data = {}
    for parameter in data:
        longname = parameters[parameter]['longname']
        new_data[longname] = {}
        for key in data[parameter]:
            new_data[longname][key[8:]] = data[parameter][key]
    pprint(new_data)
    return new_data


if __name__ == '__main__':
    longitude_ = 37.63
    latitude_ = 55.74
    data_ = get_data(longitude_, latitude_, date(2022, 6, 5))

    time_ = list(range(0, 24))

    for parameter_ in data_:
        plt.plot(time_, data_[parameter_].values(), label=parameter_)
        plt.legend()
        plt.show()
