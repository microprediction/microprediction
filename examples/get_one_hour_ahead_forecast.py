from microprediction import MicroReader
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt


def to_density(cdf):
    """  """
    # CDF is a fast, noisy O(1) approximation so this isn't the greatest
    dys = np.diff([0] + cdf['y'])
    dxs = np.diff([cdf['x'][0] - 1.0] + cdf['x'])
    dsty = [dy / dx for dx, dy in zip(dxs, dys)]
    return [d / sum(dsty) for d in dsty]


if __name__=="__main__":
    mr = MicroReader()
    HOUR = mr.DELAYS[3]
    cdf = mr.get_cdf(name='altitude.json', delay=HOUR)
    # plt.plot(cdf['x'], cdf['y'])
    plt.plot(cdf['x'], to_density(cdf))
    plt.show()
    print('https://www.microprediction.org/stream_dashboard.html?stream=altitude.json')