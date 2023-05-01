import matplotlib.pyplot as plt


def show_plot(x, data1, data2, save=False):
    plt.plot(x, [r[:] for r in data1], color='r', label='sun')
    plt.plot(x, [r[:] for r in data2], color='g', label='solar panel')

    plt.xlabel('Time, hours')
    plt.ylabel('Angle, degrees')
    plt.title('Plot')

    plt.legend()
    plt.show()

    if save:
        pass
