try:
    from credentials import ALLOSOME_CAMEL as WRITE_KEY
except ImportError:
    try:
        from microprediction.config_private import ALLOSOME_CAMEL as WRITE_KEY
    except ImportError:
        raise Exception('This example provided for transparency only')

# An example of using one stream to create another with different temporal aggregation
# Here we publish the daily mean of a stream (or rather, the difference of two daily stream means)

from microprediction import MicroWriter
import numpy as np
from microprediction.live.faang import NAAFG_NAMES

BENCHMARK_NAME = 'gnaaf_01234.json'

mw = MicroWriter(write_key=WRITE_KEY)

if __name__=='__main__':
    benchmark_returns = mw.get_recent_lagged_values(name=BENCHMARK_NAME, seconds=60*60*24)
    for name in NAAFG_NAMES:
        lagged_values = mw.get_recent_lagged_values(name=name, seconds=60*60*24 )
        net_return = np.nanmean(lagged_values) - np.mean(benchmark_returns)
        daily_name = name.replace('naafg','daily_naafg')
        mw.set(name=daily_name, value=net_return)
