from microprediction.config_private import LEGLESS_OCELOT as WRITE_KEY
from microprediction.config_private import IEX_KEY
from microprediction.polling import MultiChangePoll
from microprediction.live.iex import iex_latest_prices
import math
import numpy as np


# Creates a collection of streams related to stocks and portfolios of the same


FAANG = ['fb','aapl','amzn','nflx','googl']
TICKERS = FAANG

N_TICKERS= len(TICKERS)


from itertools import combinations_with_replacement
comb = list(combinations_with_replacement(range(N_TICKERS), r=5))


def weights_from_comb(c):
    w = 0.75*np.ones(N_TICKERS)/N_TICKERS
    for ndx in c:
        w[ndx]+=0.25/N_TICKERS
    return w


def name_from_comb(c):
    return 'gnaaf_'+''.join([ str(cj) for cj in c]) + '.json'


comb_weights_names = [ (c, weights_from_comb(c), name_from_comb(c)) for c in comb ]
GNAAF = [ name_from_comb(c) for c in comb]


def scaled_log_faang():
    sp = iex_latest_prices(tickers=FAANG, api_key=IEX_KEY)
    return [1000 * math.log(v) for v in sp]


def scaled_portfolio_return(changes, w:[float]):
    """
       Compute scaled portfolio log changes from scaled asset log changes
    """
    w = np.array(w)/np.sum(w)   # Ensure weights normalized
    f = np.exp( changes/1000.)  # Multiplicative increase in wealth
    w_post = np.inner( w, f)    # Posterior unit portfolio wealth
    change = 1000*math.log( w_post )
    return change


def change_func(changes):
    return [scaled_portfolio_return(changes,w) for _,w,_ in comb_weights_names ]


if __name__=='__main__':
    faang_names = [ 'faang_'+ticker+'.json' for ticker in TICKERS ]
    names = faang_names + GNAAF

    mcp = MultiChangePoll(write_key=WRITE_KEY, names = names, interval=5, func=scaled_log_faang, with_copulas=False,
                          change_func=change_func)
    mcp.set_repository('https://github.com/microprediction/microprediction/tree/master/stream_examples_stocks')
    mcp.run()
