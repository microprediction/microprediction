
from microprediction.live.xraytickers import XRAY_TICKERS
from microprediction.live.iex import iex_common_stock, iex_latest_prices
from microprediction.config_private import IEX_KEY
import numpy as np
import math
from getjson import getjson


def xray_portfolios():
    """ Retrieve xray portfolios """
    data = getjson('https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xrayportfolios.json')
    return [ data[str(i)] for i in range(len(data)) ]

if False:
    XRAY_PORTFOLIOS = xray_portfolios()

NUM_PORTFOLIOS = 1500
XRAY_PORTFOLIO_NAMES = ['xray_' + str(i) for i in range(NUM_PORTFOLIOS)]


def normalize(w):
    return [ wi/sum(w) for wi in w]


def create_xray_portfolios():
    # One-off determination of portfolio weights, as perturbations of pseudo-index
    common = iex_common_stock(tickers=XRAY_TICKERS, api_key=IEX_KEY)
    print(common)
    prices = iex_latest_prices(tickers=XRAY_TICKERS, api_key=IEX_KEY)
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
    CREATING = False
    if CREATING:
        # DON'T DO THIS ... SUPPOSED TO BE ONE-OFF
        create_xray_portfolios()
    else:
        portfolios = xray_portfolios()
        print(len(portfolios))

