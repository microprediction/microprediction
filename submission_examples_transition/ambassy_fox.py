try:
   from credentials import AMBASSY_FOX as WRITE_KEY
except:
   print('You did not provide a key so I am creating you a new identity. Be very patient.')
   from microprediction import new_key
   WRITE_KEY = new_key(difficulty=11)
   print(WRITE_KEY)
   print('Visit www.microprediction.org and place your key in the dashboard')
   
  
from microprediction import MicroWriter
from pprint import pprint
import numpy as np
import time


verbose = False

def values_from_lagged(lagged_values:[float], num_predictions=225)->[float]:
    """
        Produce 225 guesses of the next number based on lagged values
        Alter this as you see fit
    """
    def sorta_close(current_lags, prior_lags, rtol,atol):
        # Might want to mess with this
        return np.allclose(a=current_lags,b=prior_lags,rtol=rtol,atol=atol)

    lags = [20,10,5,4,3,2,1]
    emphasis = [l**2 for l in lags] # integer
    values = list()
    rtol = 1e-4
    atol = 1e-8
    while len(values)<num_predictions:
        rtol = rtol*2
        atol = atol*2
        for d,emp in zip(lags,emphasis):
            current_lags = lagged_values[:d]
            for k in range(1,len(lagged_values)-d):
                prior_lags = lagged_values[k:k+d]
                future_val = lagged_values[k-1]
                if sorta_close(current_lags=current_lags,prior_lags=prior_lags,rtol=rtol, atol=atol):
                    for _ in range(emp):
                        values.append(future_val + atol*np.random.randn() )

    jiggered = list(set( [ v + 0.00001*np.random.randn() for v in values]))
    return sorted(jiggered[:num_predictions])

def fix_lagged(x):
    while x>1e7:
        x = x/100.0
    return x

def submit_predictions(writer,horizons_to_avoid):
    """
        Example of creating and submitting predictions for the next meme stock
    """
    names = [ nm for nm in mw.get_stream_names() if not '~' in nm ][:10]  # Start small
    mw.set_repository('https://github.com/microprediction/microprediction/blob/master/submission_examples_transition/ambassy_fox.py')
    for name in names:
        lagged_values = mw.get_lagged_values(name=name)
        if len(lagged_values)>mw.num_predictions:
            lagged_values = [ fix_lagged(x) for x in lagged_values]
            values = values_from_lagged(lagged_values=lagged_values, num_predictions=mw.num_predictions)
            for delay in mw.DELAYS:
                horizon = mw.horizon_name(name=name,delay=delay)
                if horizon not in horizons_to_avoid:
                   try:
                       writer.submit(name=name,values=values,delay=delay)
                   except Exception as e:
                       print(e)
                       pprint(values)
                   time.sleep(0.5)


if __name__=='__main__':
    mw = MicroWriter(write_key=WRITE_KEY)
    performance = mw.get_performance()
    horizons_to_avoid = [h for h,b in performance.items() if b<-abs(stop_loss) ]
    mw.cancel_worst_active(stop_loss=stop_loss)

    # Assumes this script will be run hourly
    for _ in range(17):
        submit_predictions(writer=mw,horizons_to_avoid=horizons_to_avoid)
        time.sleep(60*3)
