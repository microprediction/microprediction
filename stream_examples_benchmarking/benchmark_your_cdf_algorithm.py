from microconventions import animal_from_key
import time
from microprediction import MicroWriter
from momentum import var_init, var_update
from tdigest import TDigest
import math
import numpy as np

# See also https://github.com/microprediction/microprediction/blob/master/notebook_examples_blog/benchmark_any_model_against_microprediction.ipynb

# Part (1) ------ Stuff you need to change -----------------
#
# You need a write key
# See https://microprediction.github.io/microprediction/writekeys.html

try:
    from credentials import LAZY_DAMSELFLY as WRITE_KEY # <--- Edit this
except ImportError:
    raise NotImplementedError('you need a write key')
print(WRITE_KEY)
ANIMAL = animal_from_key(WRITE_KEY)
NAME = 'ricky_bobby_' + ANIMAL.replace(' ','_').lower() + '.json'
URL = 'https://www.microprediction.org/stream_dashboard.html?stream='+NAME.replace('.json','')
print('This script will create the stream '+NAME+' visible at '+URL)  # <--- Name of the new stream you will be creating



# Part (2) ---- Put your model here -----------------------

def predict(lagged_values):
    """
        Replace this with your model. It is merely an example.
    """
    import numpy as np
    from microconventions.stats_conventions import StatsConventions
    from microprediction import MicroReader
    padded = [-1, 0, 1] + list(lagged_values) + list(lagged_values[:5]) + list(lagged_values[:15])
    devo = np.std(padded)
    values = sorted(
        [devo * StatsConventions.norminv(p) + 0.001 * np.random.randn() for p in MicroReader().percentiles()])
    nudged = StatsConventions.nudged(values)
    return nudged




def something_measured():
    """
        Replace this with your own instrumented quantity
    """
    import time
    import math
    import numpy as np
    x = math.sin((time.time()-1667937389)/(60*117.453))
    noise = np.random.randn()*abs(x)*0.25 + np.random.randn()*0.15
    return x + noise


# ---- Part (3)  Optionally change the method of evaluation -------


def robust_log_like(guesses, value, show=False):
    """ Interpret a finite list of guesses as a distribution and assign
        a quasi-likelihood. There's no perfect way ... I do not care ...
        you wanted this "horse race" not me.
    """

    # Induce CDF from stochastic gen tdigest
    h = (1e-4 + max(guesses) - min(guesses)) / len(guesses)
    digest = TDigest()
    bumped_guesses = list()
    for _ in range(500):
        bumped_guesses.extend([x + np.random.randn() * h / 3 for x in guesses])

    digest.batch_update(bumped_guesses)
    eps = 1e-3
    prob = (digest.cdf(value + eps) - digest.cdf(value - eps) + 1e-10) / eps
    return math.log(prob)


robust_log_like([1, 1.2, 3, 4, 4.5, 4.6, 4.8], 4.6, show=True)

if __name__=='__main__':


    WARMUP = 500
    mw = MicroWriter(write_key=WRITE_KEY)
    PARTICIPATE = True  # Set to False to match your dark heart

    market_var = var_init()  # Tracks running mean/var
    model_var = var_init()
    guesses = None
    market_guesses = None

    # Start the value changes
    MINUTE = 60  # Should be 60 but make smaller for testing

    for t in range(WARMUP):
        time.sleep(5 * MINUTE)
        prev_value = something_measured()
        time.sleep(15 * MINUTE)
        change = something_measured() - prev_value
        mw.set(name=NAME, value=change)
        print('Published ' + str(change) + ' to ' + URL, flush=True)
        prev_change = change

    while True:
        time.sleep(5 * MINUTE)
        prev_value = something_measured()

        # Make next predictions, and also get market's prediction
        lagged_values = mw.get_lagged_values(name=NAME)
        print('    predicting ...')
        model_guesses = predict(lagged_values=lagged_values)
        # Maybe participate too?  Here comes the philosophical debate
        if PARTICIPATE:
            # predict 15 minute horizon
            mw.submit(name=NAME, values=guesses, delay=mw.DELAYS[2])
            time.sleep(5)

        # Get market predictions
        print('    retrieving market predictions ...')
        market_guesses = mw.get_own_predictions(name=NAME, delay=mw.DELAYS[2])

        # Next data point arrives
        time.sleep(15 * MINUTE)
        change = something_measured() - prev_value
        mw.set(name=NAME, value=change)
        print('Published ' + str(change))

        # Evaluate
        ll_model = robust_log_like(model_guesses, change)
        ll_market = robust_log_like(market_guesses, change)
        market_var = var_update(market_var, ll_market)
        model_var = var_update(model_var, ll_model)
        report = {'write_key':WRITE_KEY,
                  'stream':NAME,
                  'market_log_like': market_var['mean'],
                  'model_log_like': model_var['mean'],
                  'market_log_like_std': market_var['std']}
        from pprint import pprint

        if market_var['mean'] > model_var['mean']:
            report['status'] = 'market is better than your model'
        else:
            report['status'] = 'market will be better than your model sooner or later'
        pprint(report)

