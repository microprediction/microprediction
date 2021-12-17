from credentials import CYSTOSE_EEL
from microprediction import MicroWriter
from collections import Counter
from pprint import pprint
import numpy as np
import time

# This part is only needed for interpretation / logging

verbose = False
stop_loss = 25

def fix_lagged(x):
    while x>1e7:
        x = x/100.0
    return x

# Implements a quasi-transition model for the Meme stock of the hour, and others

def values_from_lagged(lagged_values:[float], num_predictions=225)->[float]:
    """
        Produce 225 guesses of the next number based on lagged values
        Alter this as you see fit
    """
    values = list()

    # Use empirical transition but start with least common
    s_current = lagged_values[0]
    transition = Counter([s for s,s_prev in zip(lagged_values,lagged_values[1:]) if (s_prev==s_current) or (np.random.rand()<0.1)]).most_common()
    for val,cnt in reversed(transition):
        for _ in range(cnt):
            values.append(val+0.0001*np.random.randn())

    # Pad with most common meme stocks as needed
    if len(values)<num_predictions:
        common = Counter(lagged_values).most_common()
        for val,cnt in common:
            for _ in range(cnt):
                values.append(val+0.0001*np.random.randn())

    return sorted(values[:num_predictions])


def submit_predictions(writer,horizons_to_avoid):
    """
        Example of creating and submitting predictions for the next meme stock
    """
    names = [ nm for nm in mw.get_stream_names() if not '~' in nm ]
    for name in names:
        lagged_values = [ fix_lagged(x) for x in mw.get_lagged_values(name=name) ]
        if len(lagged_values)>225:
            values = values_from_lagged(lagged_values=lagged_values, num_predictions=mw.num_predictions)
            for delay in mw.DELAYS:
                horizon = mw.horizon_name(name=name,delay=delay)
                if horizon not in horizons_to_avoid:
                    try:
                        mw.submit(name=name,values=values,delay=delay)
                    except:
                        print('failed to submit')
                        print(len(set(values)))
                    time.sleep(0.5)


if __name__=='__main__':
    mw = MicroWriter(write_key=CYSTOSE_EEL)
    mw.set_repository('https://github.com/microprediction/microprediction/blob/master/submission_examples_transition/cystose_eel.py')
    performance = mw.get_performance()
    horizons_to_avoid = [h for h,b in performance.items() if b<-abs(stop_loss) ]
    mw.cancel_worst_active(stop_loss=stop_loss)

    # Assumes this script will be run hourly
    for _ in range(7):
        submit_predictions(writer=mw,horizons_to_avoid=horizons_to_avoid)
        time.sleep(60*8)


