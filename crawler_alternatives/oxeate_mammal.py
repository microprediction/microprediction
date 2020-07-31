from microprediction import MicroWriter, new_key
from microprediction.samplers import exponential_bootstrap
import time
from pprint import pprint

# Example of a home spun crawler
# This does not use MicroCrawler class but instead, directly uses MicroWriter.
# It enters all the z2~ streams

try:
    from microprediction.config_private import OXEATE_MAMMAL

    WRITE_KEY = OXEATE_MAMMAL  # Replace with your own
except ImportError:
    WRITE_KEY = new_key(difficulty=10)
    print(WRITE_KEY)

ANIMAL = MicroWriter.animal_from_key(WRITE_KEY)
print(ANIMAL, flush=True)
STOP_LOSS = 25.

if __name__ == "__main__":
    mw = MicroWriter(write_key=WRITE_KEY)
    LONG = '~' + str(mw.DELAYS[-1])
    SHORT = '~' + str(mw.DELAYS[0])

    # Give up if things are going badly ... do it nicely
    for _ in range(5):
        mw.cancel_worst_active(stop_loss=STOP_LOSS, num=1)
        time.sleep(1)

    for name in mw.get_streams():
        if 'z2~' in name and (LONG in name or SHORT in name):
            num = mw.num_predictions
            z11 = '~'.join(['z1', name.split('~')[1], name.split('~')[3]])
            z12 = '~'.join(['z1', name.split('~')[2], name.split('~')[3]])
            lagged1 = mw.get_lagged_values(z11)
            lagged2 = mw.get_lagged_values(z12)
            if len(lagged1) > 500:
                z_samples = list()
                for z1, z2 in zip(lagged1, lagged2):
                    try:
                        p1 = mw.normcdf(z1)
                        p2 = mw.normcdf(z2)
                        z = mw.to_zcurve(prctls=[p1, p2])
                        z_samples.append(z)
                    except:
                        pass

                samples = exponential_bootstrap(z_samples, decay=0.001, num=mw.num_predictions, as_process=None)
                for delay in mw.DELAYS:
                    pprint(mw.submit(name=name, delay=delay, values=samples))
            time.sleep(7.28)
            print(' ', flush=True)

    # Give up if things are going badly ... do it nicely
    for _ in range(100):
        mw.cancel_worst_active(stop_loss=STOP_LOSS, num=1)
        time.sleep(1)
