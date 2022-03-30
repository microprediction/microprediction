try:
    from credentials import FATHOM_GAZELLE
except ImportError:
    try:
        from microprediction.config_private import FATHOM_GAZELLE
    except ImportError:
        raise Exception('This example provided for transparency only')
import time

# An example of using one stream to create another with different temporal aggregation
# Here we publish the daily mean of a stream

from microprediction import MicroWriter
import numpy as np

WEIGHTS = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]

fathom = MicroWriter(write_key=FATHOM_GAZELLE)

if __name__=='__main__':
    for w in WEIGHTS:
        name = 'c2_info_minus_rebalanced_'+str(w)+'.json'
        lagged = fathom.get_lagged(name=name)
        t_cutoff = time.time()-60*60*24
        lagged_values = [ v for (t,v) in lagged if t>t_cutoff]
        lagged_mean = np.nanmean(lagged_values)
        fathom.set(name='c2_daily_info_minus_rebalanced_'+str(w)+'.json',value=lagged_mean)