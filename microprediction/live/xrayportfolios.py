from microprediction.live.xraytickers import get_xray_tickers
from microprediction.live.iex import iex_latest_prices, iex_common_stock_with_balance_sheet_tickers
import numpy as np
import math
from getjson import getjson
from microprediction.whereami import TOP
import os
import json
import math


SIZE_TILT_COEF = 0.1
RANK_TILT_COEF = 0.1
LOG_TILT_COEF = 0.1
TILE_NDX = [-2,-1,0,1,2]  # Must be odd
RANK_NDX = TILE_NDX
LOG_NDX = TILE_NDX
NUM_SIZE_PORTFOLIOS = len(TILE_NDX)
NUM_RANK_PORTFOLIOS = len(RANK_NDX)
NUM_LOG_PORTFOLIOS = len(LOG_NDX)
NUM_PORTFOLIOS = NUM_SIZE_PORTFOLIOS + NUM_RANK_PORTFOLIOS
NDX_CAP = (NUM_RANK_PORTFOLIOS-1)/2                       # The index of the cap weight portfolio
NDX_ONE_OVER_N = (NUM_RANK_PORTFOLIOS-1)/2 + NUM_SIZE_PORTFOLIOS + NUM_LOG_PORTFOLIOS     # The index of the 1/n portfolio

XRAY_PORTFOLIO_NAMES = ['xray_' + str(i)+'.json' for i in range(NUM_PORTFOLIOS)]
XRAY_COMMON_JSON = os.path.join(TOP, 'live', 'xrayportfolios.json')

from microprediction.live.xraytickers import STOCK_THRESHOLD


def normalize(w):
    return [ wi/sum(w) for wi in w]


def create_xray_portfolios():
    # One-off determination of portfolio weights, as perturbations of pseudo-index
    from microprediction.live.iexcredentials import get_iex_key
    IEX_KEY = get_iex_key()
    tickers = get_xray_tickers()
    num_tickers = len(tickers)
    prices = iex_latest_prices(tickers=tickers, api_key=IEX_KEY)
    common = iex_common_stock_with_balance_sheet_tickers(api_key=IEX_KEY, tickers=tickers, return_tickers=False, threshold=0.5*STOCK_THRESHOLD)
    norm_common = normalize(common)
    norm_cap = normalize([price * cm for price, cm in zip(prices, norm_common)])
    centered_cap = [ (nc-np.mean(norm_cap))/np.std(norm_cap) for nc in norm_cap ]

    norm_log = normalize([ math.log(price * cm) for price, cm in zip(prices, norm_common)])
    centered_log = [(nc - np.mean(norm_log)) / np.std(norm_log) for nc in norm_log]

    norm_rank = normalize([i for i in range(num_tickers)])
    centered_rank = [ (nr - np.mean(norm_rank))/np.std(norm_rank) for nr in norm_rank ]

    xray_portfolios = list()
    for ndx in TILE_NDX:
        cap_tilt = normalize([math.exp(nc * SIZE_TILT_COEF * ndx) for nc in centered_cap])
        xray_portfolios.append(cap_tilt)

    for ndx in LOG_NDX:
        log_tilt = normalize([math.exp(lc * LOG_TILT_COEF * ndx) for lc in centered_log])
        xray_portfolios.append(log_tilt)

    for ndx in RANK_NDX:
        rank_tilt = normalize([math.exp(nr * RANK_TILT_COEF * ndx) for nr in centered_rank])
        xray_portfolios.append(rank_tilt)

    xray_portfolios_dict = dict([(k, p) for k, p in enumerate(xray_portfolios)])

    with open(XRAY_COMMON_JSON, 'wt') as fp:
        json.dump(obj=xray_portfolios_dict, fp=fp)


def get_xray_portfolios():
    """ Retrieve xray portfolios """
    data = getjson('https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json')
    return [ data[str(i)] for i in range(len(data)) ]


if __name__=='__main__':
    CREAT_PORTFOLIOS = True
    if CREAT_PORTFOLIOS:
        # DON'T DO THIS ... SUPPOSED TO BE ONE-OFF
        create_xray_portfolios()
    else:
        portfolios = get_xray_portfolios()
        print(np.shape(portfolios))
        # Check they are all there
        tickers = get_xray_tickers()
        n_tickers = len(tickers)
        assert n_tickers == np.shape(portfolios)[1]


