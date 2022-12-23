import math
from microprediction.live.iex import iex_latest_prices, iex_common_stock_with_balance_sheet_tickers
import os
import json
from getjson import getjson
from microprediction.whereami import TOP
from microprediction.live.iex import iex_common_stock_with_balance_sheet_tickers
from collections import OrderedDict

RDPS_DESCRIPTIONS = OrderedDict({'e':'energy',
                                 'c':'communication',
                                 'y':'discretionary',
                                 'p':'discretionary',
                                 'f':'financials',
                                 'v':'health',
                                 'i':'industrials',
                                 'b':'materials',
                                 're':'real estate',
                                 'k':'technology',
                                 'u':'utilities'})

# 2022-12-07
RDPS_CAPS_DICT = {'energy':1638445299830,
             'materials':900434969540,
             'industrials':2824657615645,
             'discretionary':3377812181150,
             'staples':2358952321990,
             'health':5196971888210,
             'financials':3788386237860,
             'technology':8626912590550,
             'communication':2439153232630,
             'utilities':1015883727160,
             'real estate':891892003410}

# 2022-12-07
RDPS_PRICES_DICT = {'energy':85.12,
             'materials':82.10,
             'industrials':99.30,
             'discretionary':138.70,
             'staples':76.07,
             'health':138.52,
             'financials':34.59,
             'technology':129.60,
             'communication':49.40,
             'utilities':70.74,
             'real estate':38.10}


RDPS_TICKERS = ['xl'+suffix for suffix in RDPS_DESCRIPTIONS.keys() ]
RDPS_RATIOS = [ RDPS_CAPS_DICT[desc]/RDPS_PRICES_DICT[desc] for e,desc in RDPS_DESCRIPTIONS.items() ]
RDPS_GENERIC_NAMES = [ 'rdps_' + ticker + '.json' for ticker in RDPS_TICKERS ]
RDPS_TICKERS_JSON = os.path.join(TOP,'live', 'rdpstickers.json')
RDPS_TICKERS_REVERSE_JSON = os.path.join(TOP ,'live' ,'rdpstickersreverse.json')


def save_rdps_tickers(tickers):
    tickers_dict = dict([(k, ticker) for k, ticker in enumerate(tickers)])
    with open(RDPS_TICKERS_JSON, 'wt') as fp:
        json.dump(obj=tickers_dict, fp=fp)
    tickers_reverse_dict = dict(sorted([(ticker, k) for k, ticker in enumerate(tickers)]))
    with open(RDPS_TICKERS_REVERSE_JSON, 'wt') as fp:
        json.dump(obj=tickers_reverse_dict, fp=fp)


def get_rdps_tickers() -> [str]:
    """ Retrieve xray tickers """
    url = 'https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/rdpstickers.json'
    data = getjson(url, failover_url=url)
    return [data[str(i)] for i in range(len(data))]


def rdps_index_fraction(prices):
    """ Return percentage of index by cap, given a set of current prices for the sector ETFs """
    assert len(prices)==len(RDPS_RATIOS)
    raw = [ p*r for p,r in zip(prices,RDPS_RATIOS)]
    return [ w/sum(raw) for w in raw]


if __name__=='__main__':
    if False:
        save_rdps_tickers(RDPS_TICKERS)
    print(RDPS_SHARES)