import math
from microprediction.live.iex import iex_latest_prices, iex_common_stock_with_balance_sheet_tickers
import os
import json
from getjson import getjson
from microprediction.whereami import TOP
from microprediction.live.iex import iex_common_stock_with_balance_sheet_tickers


XRAY_TICKERS_JSON = os.path.join(TOP,'live', 'xraytickers.json')
XRAY_TICKERS_REVERSE_JSON = os.path.join(TOP ,'live' ,'xraytickersreverse.json')

STOCK_THRESHOLD = 100*1000*1000*1000


def reasonable_threshold():
    # Get common stock value for VSAT, the smallest company in Russell 1000
    from microprediction.live.iexcredentials import get_iex_key
    tickers = ['vsat']
    common = iex_common_stock_with_balance_sheet_tickers(api_key=get_iex_key(), return_tickers=False, tickers=tickers)
    print(common)
    return common


def create_xray_tickers_json():
    """
       Create JSON file storing "official" list of tickers using in the x-ray experiment
    """
    tickers = iex_common_stock_with_balance_sheet_tickers(api_key=IEX_KEY, return_tickers=True, threshold=STOCK_THRESHOLD)
    tickers_dict = dict([(k, ticker) for k, ticker in enumerate(tickers)])
    with open(XRAY_TICKERS_JSON, 'wt') as fp:
        json.dump(obj=tickers_dict, fp=fp)
    tickers_reverse_dict = dict( sorted( [(ticker, k) for k, ticker in enumerate(tickers)]))
    with open(XRAY_TICKERS_REVERSE_JSON, 'wt') as fp:
        json.dump(obj=tickers_reverse_dict, fp=fp)


def get_xray_tickers() -> [str]:
    """ Retrieve xray tickers """
    url = 'https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json'
    data = getjson(url, failover_url=url)
    return [data[str(i)] for i in range(len(data))]


def get_xray_stock_names():
    return [ 'yarx_'+ticker+'.json' for ticker in get_xray_tickers() ]


if __name__ == '__main__':
    CREATE_TICKERS = True
    if CREATE_TICKERS:
        from microprediction.live.iexcredentials import get_iex_key
        IEX_KEY = get_iex_key()
        create_xray_tickers_json()
