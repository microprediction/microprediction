try:
    from credentials import FATHOM_GAZELLE
except ImportError:
    raise Exception('This example provided for transparency only')

# An example of using one stream to create another with different temporal aggregation

from microprediction import MicroWriter
import numpy as np

WEIGHTS = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]

fathom = MicroWriter(write_key=FATHOM_GAZELLE)

if __name__=='__main__':
    for w in WEIGHTS:
        lagged_values = fathom.get_lagged_values(name='c2_info_minus_rebalanced_'+str(w)+'_diff.json')
        lagged_mean = np.nanmean(lagged_values[:100])
        fathom.set(name='c2_daily_info_minus_rebalanced_'+str(w)+'.json',value=lagged_mean)