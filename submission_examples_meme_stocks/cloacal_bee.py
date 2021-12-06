from credentials import CLOACAL_BEE
from microprediction import MicroWriter
from pprint import pprint
import numpy as np
import time
import math


def values_from_lagged(lagged_values:[float], num_predictions=225)->[float]:
    """
        Produce 225 guesses of the next number based on lagged values
        Alter this as you see fit
    """
    s_before  = lagged_values[1]
    s_current = lagged_values[0]
    two_transition = [s for s,s_prev,s_prev_prev in zip(lagged_values,lagged_values[1:],lagged_values[2:]) if ((s_prev==s_current) and (s_prev_prev==s_before)) ]
    one_transition = [s for s,s_prev in zip(lagged_values,lagged_values[1:]) if (s_prev==s_current) or (np.random.rand()<0.1)]
    zero_transition = [s for s in lagged_values]
    print({'two_trans':two_transition,
           'one_trans':one_transition})

    n_rep = int(math.ceil(125/(1+len(two_transition))))
    all_transition = two_transition*n_rep + one_transition*2 + zero_transition
    values = sorted([ v + 0.00001*np.random.randn() for v in all_transition[:num_predictions]])
    n_unique = len(set(values))
    assert n_unique==num_predictions,'hmmm that no good'
    return values

def fix_lagged(x):
    while x>1e7:
        x = x/100.0
    return x

def submit_predictions():
    """
        Example of creating and submitting predictions for the next meme stock
    """
    mw = MicroWriter(write_key=CLOACAL_BEE)
    names = [ nm for nm in mw.get_stream_names() if 'meme' in nm and not '~' in nm ]
    mw.set_repository('https://github.com/microprediction/microprediction/blob/master/submission_examples_meme_stocks/cloacal_bee.py')
    for name in names:
        lagged_values = mw.get_lagged_values(name=name)
        if len(lagged_values)>225:
            lagged_values = [ fix_lagged(x) for x in lagged_values]
            values = values_from_lagged(lagged_values=lagged_values, num_predictions=mw.num_predictions)
            for delay in mw.DELAYS:
                res = mw.submit(name=name,values=values,delay=delay)
                pprint(res)
                time.sleep(0.5)




if __name__=='__main__':
    # Assumes this script will be run hourly
    for _ in range(7):
        submit_predictions()
        time.sleep(60*8)
