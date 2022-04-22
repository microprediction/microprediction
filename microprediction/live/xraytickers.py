import math
from microprediction.live.iex import iex_latest_prices, iex_common_stock_with_balance_sheet_tickers
import os
import json
from getjson import getjson
from microprediction.whereami import TOP

XRAY_TICKERS_JSON = os.path.join(TOP ,'live' ,'xraytickers.json')


def create_xray_tickers_json():
    """
       Create JSON file storing "official" list of tickers using in the x-ray experiment
    """
    tickers = iex_common_stock_with_balance_sheet_tickers(api_key=IEX_KEY, return_tickers=True)
    tickers_dict = dict([(k, ticker) for k, ticker in enumerate(tickers)])
    with open(XRAY_TICKERS_JSON, 'wt') as fp:
        json.dump(obj=tickers_dict, fp=fp)


def get_xray_tickers() -> [str]:
    """ Retrieve xray tickers """
    data = getjson('https://raw.githubusercontent.com/microprediction/microprediction/master/microprediction/live/xraytickers.json')
    return [data[str(i)] for i in range(len(data))]



if __name__ == '__main__':
    CREATE_TICKERS = True
    if CREATE_TICKERS:
        from microprediction.live.iexcredentials import get_iex_key
        IEX_KEY = get_iex_key()
        create_xray_tickers_json()
