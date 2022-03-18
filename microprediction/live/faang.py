import numpy as np
import os
import json
import math
from itertools import combinations_with_replacement
from microprediction.live.iex import iex_latest_prices

# A few conventions used by FAANG streams


FAANG_TICKERS = ['fb', 'aapl', 'amzn', 'nflx', 'googl']
FAANG_NAMES = ['faang_' + ticker + '.json' for ticker in FAANG_TICKERS] # Stream names
N_FAANG = len(FAANG_TICKERS)
FAANG_COMBINATIONS = list(combinations_with_replacement(range(N_FAANG), r=5))


def iex_scaled_log_faang(api_key:str):
    """
       Retrieve live prices for FAANG and transform
       api_key: An IEX api key
    """
    sp = iex_latest_prices(tickers=FAANG_TICKERS, api_key=api_key)
    return [1000 * math.log(v) for v in sp]


def portfolio_from_combination(c):
    """
       Converts a combination like 1,1,1,2,3 into weighted portfolio
    """
    n = len(c)
    w = 0.75*np.ones(n)/n
    for ndx in c:
        w[ndx]+=0.25/n
    return w


def readable_portfolio_from_combination(c,tickers):
    w = portfolio_from_combination(c)
    return 'Portfolio comprising '+', '.join( [ str(round(wi*100,0))+'% '+ticker for wi,ticker in zip(w,tickers)])


def gnaff_name_from_combination(c):
    return 'gnaaf_'+''.join([ str(cj) for cj in c]) + '.json'


GNAAF_NAMES = [gnaff_name_from_combination(c) for c in FAANG_COMBINATIONS]
GNAAF_WEIGHTS = [ portfolio_from_combination(c) for c in FAANG_COMBINATIONS]
GNAAF_LISTING = dict([(readable_portfolio_from_combination(c, tickers=FAANG_TICKERS), 'https://www.microprediction.org/stream_dashboard.html?stream=' + gnaff_name_from_combination(c).replace('.json', '')) for c in FAANG_COMBINATIONS])


def create_listing_file():
    """
       Updates the stream listing
    """
    from microprediction.whereami import ROOT
    fn = os.path.join(ROOT, 'stream_examples_faang', 'stream_list.json')
    with open(fn,'wt') as fh:
        json.dump(GNAAF_LISTING,fh)


def scaled_portfolio_return(changes, w:[float]):
    """
       Compute scaled portfolio log changes from scaled asset log changes
    """
    w = np.array(w)/np.sum(w)   # Ensure weights normalized
    f = np.exp( np.array(changes)/1000.)  # Multiplicative increase in wealth
    w_post = float( np.inner( w, f) )    # Posterior unit portfolio wealth
    portfolio_change = 1000*math.log( w_post )
    return portfolio_change



if __name__=='__main__':
    create_listing_file()
