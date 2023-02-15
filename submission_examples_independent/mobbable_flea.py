from microprediction import MicroWriter
from microprediction.live.rdpstickers import get_rdps_tickers, RDPS_GENERIC_NAMES
import numpy as np
from microconventions.stats_conventions import StatsConventions
import time
from getjson import getjson
from scipy.stats import iqr
from tdigest import TDigest
import math

# Example of a prediction script that only needs to be run sporadically, since here it is assumed the
# data comprises independent identically distributed samples.

# For each stream this performs a somewhat lazy resampling, and then scales using options data
# Think of it as a global forecast


# Every algorithm submitting requires a WRITE_KEY. Alter this part.
try:
    from credentials import MOBBABLE_FLEA as WRITE_KEY
except:
    raise EnvironmentError('You need a write key. See https://www.microprediction.com/private-keys for explanation')



if __name__=='__main__':
    NAMES = ['rdps_spy.json'] + RDPS_GENERIC_NAMES
    print({'NAMES':NAMES})

    # Create a writer, and give the system a backlink for the convenience of others (edit the repo to your own if you like)
    mw = MicroWriter(write_key=WRITE_KEY)
    ANIMAL = mw.animal_from_key(WRITE_KEY)
    REPO = 'https://github.com/microprediction/microprediction/blob/master/submission_examples_independent/' + ANIMAL.lower().replace(
        ' ', '_') + '.py'
    mw.set_repository(url=REPO)

    # Grab stale implied vols
    implied_vols = getjson('https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/etfimpliedvols.json')


    # Infer tickers
    tickers = [ name.split('_')[1].replace('.json','') for name in NAMES ]
    print(tickers)

    # Get the approximate volatility premium (multiplier)
    lagged_data = dict([(name,mw.get_lagged_values(name=name)) for name in NAMES ])
    lagged_data_everyone = [x for nm,lgs in lagged_data.items() for x in lgs]  # Flatten into a global lagged list
    lagged_data_everyone_recent = [x for nm,lgs in lagged_data.items() for x in lgs[:50]]

    iqrs = [ iqr(lagged_data[name]+[-1,1]) for name in NAMES ]
    median_iqr = np.median(iqrs)
    median_implied_vol = np.median(list(implied_vols.values()))
    iqr_multiplier = median_iqr / median_implied_vol
    print({'iqr_multiplier':iqr_multiplier})

    def jiggle(xs):
        return [ x + 0.01*np.random.randn() for x in xs ]

    for name, ticker in zip(NAMES,tickers):
        # Use lagged values to boostrap an approximate distribution with a little recency weighting
        lagged_values = 30*lagged_data[name] + 5*lagged_data_everyone_recent + lagged_data_everyone
        padded = [-1, 0, 1 ] + list(jiggle(lagged_values))

        if True:
            # Rescale? Suit yourself
            scale = (implied_vols[ticker]/median_implied_vol)*(median_iqr/iqr(padded))
            padded = [ math.sqrt(scale)*x for x in padded ]

        # Borrow tdigest for percentiles
        digest = TDigest()
        digest.batch_update(padded)
        values = [ digest.percentile(p*100) for p in mw.percentiles() ]
        nudged = StatsConventions.nudged(values)  # <-- Make tiny changes to stay clear of others' points
        for delay in mw.DELAYS[-1:]:
            mw.submit(name=name, values=nudged, delay=delay)
            stream_url = 'https://www.microprediction.org/stream_dashboard.html?stream='+name.replace('.json','')+'&horizon='+str(delay)
            print(stream_url)
            time.sleep(1)  # <-- Out of consideration for the system

