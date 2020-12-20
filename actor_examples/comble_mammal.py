from microprediction.config_private import COMBLE_MAMMAL
from microprediction import MicroWriter
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt

WRITE_KEY = COMBLE_MAMMAL
ANIMAL = MicroWriter.animal_from_key(WRITE_KEY)
REPO = 'https://github.com/microprediction/microprediction/blob/master/copula_examples/' + ANIMAL.lower().replace(
    ' ', '_') + '.py'
import time
import warnings
warnings.filterwarnings('ignore')
from copulas.multivariate import GaussianMultivariate
import pandas as pd
VERBOSE = False

# We simply loop over all z3~ streams
# This script might be run once every hour or so
# Remark: It's lazy to just sample synthetic data
# Some more evenly spaced sampling would be preferable
# See https://www.microprediction.com/blog/lottery for discussion


def fit_and_sample(lagged_zvalues:[[float]],num:int, copula=None):
    """ Example of fitting a copula function, and sampling
           lagged_zvalues: [ [z1,z2,z3] ]  distributed N(0,1) margins, roughly
           copula : Something from https://pypi.org/project/copulas/
           returns: [ [z1, z2, z3] ]  representative sample

    """

    df = pd.DataFrame(data=lagged_zvalues)
    if copula is None:
        copula = GaussianMultivariate()
    copula.fit(df)
    synthetic = copula.sample(num)
    return synthetic.values.tolist()


if __name__ == "__main__":
    mw = MicroWriter(write_key=WRITE_KEY)

    for name in mw.get_streams():
        if 'z3~' in name:
            for delay in mw.DELAYS:
                lagged_zvalues = mw.get_lagged_zvalues(name=name, count= 5000)
                if len(lagged_zvalues)>20:
                    zvalues = fit_and_sample(lagged_zvalues=lagged_zvalues, num=mw.num_predictions)
                    res = mw.submit_zvalues(name=name, zvalues=zvalues, delay=delay )

