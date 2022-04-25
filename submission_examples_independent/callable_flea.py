from microprediction import MicroWriter
from microprediction.live.xraytickers import get_xray_stock_names
from microprediction.live.xrayportfolios import XRAY_PORTFOLIO_NAMES
import numpy as np
from microconventions.stats_conventions import StatsConventions
import time

# Example of a prediction script that only needs to be run sporadically, since here it is assumed the
# data comprises independent identically distributed samples

# Every algorithm submitting requires a WRITE_KEY. Alter this part.
try:
    from microprediction.config_private import MOBBABLE_FLEA as WRITE_KEY
except:
    raise EnvironmentError('You need a write key. See https://www.microprediction.com/private-keys for explanation')


if __name__=='__main__':
    NAMES = get_xray_stock_names() + XRAY_PORTFOLIO_NAMES

    # Create a writer, and give the system a backlink for the convenience of others
    mw = MicroWriter(write_key=WRITE_KEY)
    ANIMAL = mw.animal_from_key(WRITE_KEY)
    REPO = 'https://github.com/microprediction/microprediction/blob/master/submission_examples_independent/' + ANIMAL.lower().replace(
        ' ', '_') + '.py'
    mw.set_repository(url=REPO)

    # Loop over streams, making predictions
    for name in NAMES:
        lagged_values = mw.get_lagged_values(name=name)
        padded = [-1, 0, 1 ] + list(lagged_values) + list(lagged_values[:5]) + list(lagged_values[:15])
        devo = np.std(padded)
        values = sorted( [ devo*mw.norminv(p) +  0.001 * np.random.randn() for p in mw.percentiles()] )
        nudged = StatsConventions.nudged(values)
        for delay in mw.DELAYS:
            mw.submit(name=name, values=values, delay=delay)
            stream_url = 'https://www.microprediction.org/stream_dashboard.html?stream='+name.replace('.json','')+'&horizon='+str(delay)
            print(stream_url)
            time.sleep(1)  # <-- Out of consideration for the system






