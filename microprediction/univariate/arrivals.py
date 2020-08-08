from statistics import mode, StatisticsError
import numpy as np


# Placeholder for better data arrival estimation

def approx_dt(lagged_times):
    """ Crude estimate of the typical time between arrivals """
    if len(lagged_times) > 5:
        return approx_mode([abs(dt) for dt in np.diff(list(lagged_times))]) or 60
    else:
        return 60


def approx_mode(xs, ndigits=0):
    """ Mode of rounded numbers, or None """
    xr = [round(x, ndigits) for x in xs]
    try:
        return mode(xr)
    except StatisticsError:
        return None
