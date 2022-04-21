
from microprediction.live.xraytickers import XRAY_TICKERS
from microprediction.live.iex import iex_common_stock, iex_latest_prices
from microprediction.config_private import IEX_KEY
import numpy as np
import math
from getjson import getjson

tickers = XRAY_TICKERS
NUM_PORTFOLIOS = 2000


def xray_portfolios():
    """ Retrieve xray portfolios """
    data = getjson('https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json')
    return [ data[i] for i in range(len(data)) ]


def normalize(w):
    return [ wi/sum(w) for wi in w]


def create_xray_portfolios():
    # One-off determination of portfolio weights, as perturbations of pseudo-index
    common = iex_common_stock(tickers=tickers, api_key=IEX_KEY)
    print(common)
    prices = iex_latest_prices(tickers=tickers, api_key=IEX_KEY)
    index_like = normalize([price * common for price, common in zip(prices, common)])
    XRAY_PORTFOLIOS = [normalize([wi * math.exp(np.random.randn()) for wi in index_like]) for _ in
                       range(NUM_PORTFOLIOS)]
    XRAY_PORTFOLIOS_DICT = dict([(k, p) for k, p in enumerate(XRAY_PORTFOLIOS)])

    from microprediction.whereami import TOP
    import os
    import json
    XRAY_COMMON_JSON = os.path.join(TOP, 'live', 'xrayportfolios.json')
    with open(XRAY_COMMON_JSON, 'wt') as fp:
        json.dump(obj=XRAY_PORTFOLIOS_DICT, fp=fp)



if __name__=='__main__':
    create_xray_portfolios()

