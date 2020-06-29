from microprediction import MicroWriter
from microprediction.samplers import exponential_bootstrap
import time
from pprint import pprint
from microprediction.config_private import OXEATE_MAMMAL

# Enters all the z2 streams

WRITE_KEY = OXEATE_MAMMAL
ANIMAL = MicroWriter.animal_from_key(WRITE_KEY)
print(ANIMAL,flush=True)
STOP_LOSS=250.

if __name__=="__main__":
    mw = MicroWriter(write_key=WRITE_KEY)
    LONG = '~'+str(mw.DELAYS[-1])
    SHORT = '~'+str(mw.DELAYS[0])

    # Give up if things are going badly ... do it nicely
    for _ in range(5):
        mw.withdraw_from_worst(stop_loss=STOP_LOSS, num=1)
        time.sleep(1)

    for name in mw.get_streams():
        if 'z2~' in name and (LONG in name or SHORT in name):
            num    = mw.num_predictions
            z11 = '~'.join(['z1', name.split('~')[1], name.split('~')[3]])
            z12 = '~'.join(['z1', name.split('~')[2], name.split('~')[3]])
            lagged1 = mw.get_lagged_values(z11)
            lagged2 = mw.get_lagged_values(z12)
            if len(lagged1)>10:
                z_samples = list()
                for z1,z2 in zip(lagged1,lagged2):
                    try:
                        p1 = mw.normcdf(z1)
                        p2 = mw.normcdf(z2)
                        z  = mw.to_zcurve(prctls=[p1,p2])
                        z_samples.append(z)
                    except:
                        pass

                samples = exponential_bootstrap( z_samples, decay=0.001, num=mw.num_predictions, as_process=None)
                pprint(mw.submit(name=name,values=samples))
            time.sleep(7.28)
            print(' ',flush=True)

    # Give up if things are going badly ... do it nicely
    for _ in range(100):
        mw.withdraw_from_worst(stop_loss=STOP_LOSS,num=1)
        time.sleep(1)
