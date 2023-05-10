import matplotlib.pyplot as plt
from pprint import pprint


def show_plot(x, data1, data2, data3, range_3, save=False):

    plt.plot(x, [r[0] for r in data1], color='#cccc00', label='sun elevation')
    plt.plot(x, [r[1] for r in data1], color='#ff3300', label='sun azimuth')

    plt.plot(x, [r[0] for r in data2], color='#009900', label='panel elevation')
    plt.plot(x, [r[1] for r in data2], color='#0000ff', label='panel azimuth')

    plt.xlabel('Time, hours')
    plt.ylabel('Angle, degrees')
    plt.title('Plot')
    plt.legend()

    plt.figure()
    plt.plot(range_3, data3)

    plt.show()

    if save:
        pass
