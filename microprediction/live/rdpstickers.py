import math
from microprediction.live.iex import iex_latest_prices, iex_common_stock_with_balance_sheet_tickers
import os
import json
from getjson import getjson
from microprediction.whereami import TOP
from microprediction.live.iex import iex_common_stock_with_balance_sheet_tickers


RDPS_DESCRIPTIONS = {'e':'energy',
         'c':'communication',
         'y':'discretionary',
         'p':'discretionary',
         'f':'financials',
         'v':'health',
         'i':'industrials',
         'b':'materials',
         're':'real estate',
         'k':'technology',
         'u':'utilities'}


RDPS_TICKERS = ['xl'+suffix for suffix in RDPS_DESCRIPTIONS.keys() ]

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



if __name__=='__main__':
    save_rdps_tickers(RDPS_TICKERS)