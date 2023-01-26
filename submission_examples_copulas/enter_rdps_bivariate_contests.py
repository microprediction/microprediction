from microprediction.config_private import COMBLE_MAMMAL
import random
import time
import warnings
warnings.filterwarnings('ignore')
from copulas.multivariate import GaussianMultivariate
import pandas as pd
from microprediction import MicroWriter
from pprint import pprint


EMAIL = "peter.cotton@microprediction.com"    # Edit
URL = None                                    # If you want your code to be public (how spirited) then please supply a link to the code on Github or elsewhere
WRITE_KEY = None                              # Edit this after you run this colab notebook the first time, to update your submissions rather than creating a new WRITE_KEY
VERBOSE = False


# Get historical data, fit a copula, and submit

def fit_and_sample(lagged_zvalues:[[float]],num:int, copula=None):
    """ Example of fitting a copula function, and sampling
           lagged_zvalues: [ [z1,z2,z3] ]  distributed N(0,1) margins, roughly
           copula : Something from https://pypi.org/project/copulas/
           returns: [ [z1, z2, z3] ]  representative sample
    """
    # Remark: It's lazy to just sample synthetic data
    # Some more evenly spaced sampling would be preferable.
    # See https://www.microprediction.com/blog/lottery for discussion

    df = pd.DataFrame(data=lagged_zvalues)
    if copula is None:
        copula = GaussianMultivariate()
    copula.fit(df)
    synthetic = copula.sample(num)
    return synthetic.values.tolist()


if __name__ == "__main__":

    # Self-register
    if WRITE_KEY is None:
        print('Creating a write key is one-off, but takes hours')
        from microprediction import new_key
        WRITE_KEY = new_key(difficulty=11)  # Better to use difficulty 12 actually

    # Create a writer and reveal your public nom de plume
    from microprediction import MicroWriter
    mw = MicroWriter(write_key=WRITE_KEY)
    ANIMAL = mw.animal_from_key(WRITE_KEY)
    if URL:
        mw.set_repository(url=URL)

    print({'private key': WRITE_KEY, 'spirit animal ': ANIMAL, 'url': URL})
    print('Paste your private key in the dashboard at https://www.microprediction.org/')

    # List the rdps bivariate streams
    NAMES = [ n for n in mw.get_stream_names() if 'z2~' in n and 'rdps' in n ]

    for name in NAMES:
        delay = mw.DELAYS[-1]  # Only submit for the 1hr horizon
        lagged_zvalues = mw.get_lagged_zvalues(name=name, count= 5000)
        if len(lagged_zvalues)>20:
            zvalues = fit_and_sample(lagged_zvalues=lagged_zvalues, num=mw.num_predictions)
            try:
                res = mw.submit_zvalues(name=name, zvalues=zvalues, delay=delay )
                if VERBOSE:
                    pprint(res)
            except Exception as e:
                print(e)
            time.sleep(1)  # Out of consideration for the system
