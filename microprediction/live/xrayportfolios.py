from microprediction.live.xraytickers import get_xray_tickers
from microprediction.live.iex import iex_latest_prices, iex_common_stock_with_balance_sheet_tickers
import numpy as np
import math
from getjson import getjson
from microprediction.whereami import TOP
import os
import json


NUM_PORTFOLIOS = 500
XRAY_PORTFOLIO_NAMES = ['xray_' + str(i)+'.json' for i in range(NUM_PORTFOLIOS)]

from microprediction.live.xraytickers import STOCK_THRESHOLD

def normalize(w):
    return [ wi/sum(w) for wi in w]


def create_xray_portfolios():
    # One-off determination of portfolio weights, as perturbations of pseudo-index
    from microprediction.live.iexcredentials import get_iex_key
    IEX_KEY = get_iex_key()
    tickers = get_xray_tickers()
    prices = iex_latest_prices(tickers=tickers, api_key=IEX_KEY)
    common = iex_common_stock_with_balance_sheet_tickers(api_key=IEX_KEY, tickers=tickers, return_tickers=False, threshold=STOCK_THRESHOLD)
    index_like = normalize([price * cm for price, cm in zip(prices, common)])
    XRAY_PORTFOLIOS = [normalize([wi * math.exp(np.random.randn()) for wi in index_like]) for _ in
                       range(NUM_PORTFOLIOS)]
    XRAY_PORTFOLIOS_DICT = dict([(k, p) for k, p in enumerate(XRAY_PORTFOLIOS)])
    XRAY_COMMON_JSON = os.path.join(TOP, 'live', 'xrayportfolios.json')
    with open(XRAY_COMMON_JSON, 'wt') as fp:
        json.dump(obj=XRAY_PORTFOLIOS_DICT, fp=fp)


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

