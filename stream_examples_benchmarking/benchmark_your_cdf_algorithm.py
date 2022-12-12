from microprediction import MicroWriter
import random
import numpy as np
from microconventions import StatsConventions

# This example illustrates how you can (slowly) benchmark any
# prediction algorithm against the microprediction oracle. You will
# have to run this script for a week or two. All good things come to
# those who wait.


# Step 0: You need a write key. See https://microprediction.github.io/microprediction/writekeys.html
try:
    from microprediction.config_private import DOOMSDAY_STOAT
except ImportError:
    raise EnvironmentError('Not a working example as is. Change to use your own write key.')

# Step 1: You need a predictive model that takes a vector of historical data and returns 225 guesses of the next value

k=1 # Number of steps ahead...keeping things simple here.

def my_brilliant_sampler(lagged_values):
    """
    :param lagged_values:  In reverse chrono order
    :return:
    """
    padded = [-1, 0, 1] + list(lagged_values) + list(lagged_values[:5]) + list(lagged_values[:15])
    devo = np.std(padded)
    values = sorted([devo * mw.norminv(p) + 0.001 * np.random.randn() for p in mw.percentiles()])
    nudged = StatsConventions.nudged(values)


def weighted_die():
    FACES=[1,2,3,4,5,6]
    return random.choices(population=FACES,weights=FACES)[0]


if __name__=='__main__':
    STREAM_NAME = 'die.json'    # <--- Change this too1
    mw = MicroWriter(write_key=DOOMSDAY_STOAT)
    value = weighted_die()
    res = mw.set(name='die.json', value=value)
    print(res)
