from microprediction.config_private import LEGLESS_OCELOT as WRITE_KEY
from microprediction.config_private import IEX_KEY
from microprediction.polling import MultiChangePoll
from microprediction.live.iex import iex_latest_prices
import math
import numpy as np
import os
import json


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


def readable_weights_from_comb(c):
    w = weights_from_comb(c)
    return 'Portfolio comprising '+', '.join( [ str(round(wi*100,0))+'% '+ticker for wi,ticker in zip(w,FAANG)])


def gnaff_name(c):
    return 'gnaaf_'+''.join([ str(cj) for cj in c]) + '.json'


comb_weights_names = [(c, weights_from_comb(c), gnaff_name(c)) for c in comb]
GNAAF = [gnaff_name(c) for c in comb]
GNAAF_LISTING = dict( [ ( readable_weights_from_comb(c), 'https://www.microprediction.org/stream_dashboard.html?stream='+gnaff_name(c).replace('.json','')) for c in comb] )

faang_names = ['faang_' + str(k) + '.json' for k, ticker in enumerate(TICKERS)]
names = faang_names + GNAAF

def scaled_log_faang():
    sp = iex_latest_prices(tickers=FAANG, api_key=IEX_KEY)
    return [1000 * math.log(v) for v in sp]


def scaled_portfolio_return(changes, w:[float]):
    """
       Compute scaled portfolio log changes from scaled asset log changes
    """
    w = np.array(w)/np.sum(w)   # Ensure weights normalized
    f = np.exp( np.array(changes)/1000.)  # Multiplicative increase in wealth
    w_post = float( np.inner( w, f) )    # Posterior unit portfolio wealth
    change = 1000*math.log( w_post )
    return change


def change_func(changes):
    return [scaled_portfolio_return(changes,w) for _,w,_ in comb_weights_names ]


def create_listing_file():
    from microprediction.whereami import ROOT
    fn = os.path.join(ROOT, 'stream_examples_faang', 'stream_list.json')

    with open(fn,'wt') as fh:
        json.dump(GNAAF_LISTING,fh)




if __name__=='__main__':
    from pprint import pprint
    create_listing_file()



    mcp = MultiChangePoll(write_key=WRITE_KEY, names = names, interval=5, func=scaled_log_faang, with_copulas=False,
                          change_func=change_func)
    mcp.set_repository('https://github.com/microprediction/microprediction/tree/master/stream_examples_stocks')
    mcp.run()
