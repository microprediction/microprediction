from microprediction.config_private import COMBLE_MAMMAL
import random
import time
import warnings
warnings.filterwarnings('ignore')
from copulas.multivariate import GaussianMultivariate
import pandas as pd
from microprediction import MicroWriter
from pprint import pprint

WRITE_KEY = COMBLE_MAMMAL


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
    ANIMAL = MicroWriter.animal_from_key(WRITE_KEY)
    REPO = 'https://github.com/microprediction/microprediction/blob/master/examples_scheduled_copulas/' + ANIMAL.lower().replace(
        ' ', '_') + '.py'
    print('This is ' + ANIMAL)
    VERBOSE = False
    mw = MicroWriter(write_key=WRITE_KEY)
    mw.set_repository(REPO) # Just polite

    NAMES = [ n for n in mw.get_stream_names() if 'z2~' in n or 'z3~' in n ]
    for _ in range(10):
        name = random.choice(NAMES)
        for delay in mw.DELAYS:
            lagged_zvalues = mw.get_lagged_zvalues(name=name, count= 5000)
            if len(lagged_zvalues)>20:
                zvalues = fit_and_sample(lagged_zvalues=lagged_zvalues, num=mw.num_predictions)
                pprint((name, delay))
                try:
                    res = mw.submit_zvalues(name=name, zvalues=zvalues, delay=delay )
                    pprint(res)
                except Exception as e:
                    print(e)
                time.sleep(1)
