# IEX stock prices
# You can get your api_key at https://iexcloud.io/
# See https://iexcloud.io/docs/api/#quote

from getjson import getjson
from pprint import pprint
import os
import json

DEFAULT_EXCHANGES = ['XNYS', 'BATS', 'ARCX', 'XASE',  'XNAS']  # XPOR


def iex_exchanges(api_key:str):
    url = 'https://cloud.iexapis.com/beta/ref-data/symbols?token=' + api_key
    data = getjson(url)
    return list(set([d['exchange'] for d in data]))


def iex_common_stock_tickers(api_key:str, exchanges=None) -> [str]:
    """ Listing of all common stock tickers """
    if exchanges is None:
        exchanges = DEFAULT_EXCHANGES
    url = 'https://cloud.iexapis.com/beta/ref-data/symbols?token='+api_key
    data = getjson(url)
    return sorted( [ d['symbol'].lower() for d in data if (d['exchange'] in exchanges) and (d['type']=='cs')])


def iex_latest_prices(tickers, api_key:str)->[float]:
    """
        Grab multiple stock prices
        IEX allows only 100 at a time
    """
    SENTINEL = 666
    def price_or_sentinel(s):
        if s is None:
            return SENTINEL
        else:
            if s.get('price') is None:
                return SENTINEL
            else:
                return s.get('price')

    if len(tickers)>100:
        tickerlists = [tickers[i:i + 100] for i in range(0, len(tickers), 100)]
        mids = [ iex_latest_prices(tickers=ticks, api_key=api_key) for ticks in tickerlists ]
        mids_flat = [item for sublist in mids for item in sublist]
        return mids_flat
    else:
        substituted = [ 'meta' if t=='fb' else t for t in tickers]
        symbols = ','.join(substituted)
        paid_url = 'https://cloud.iexapis.com/v1/stock/market/batch?types=price&symbols='+symbols+'&token=' + api_key
        print(paid_url)
        data = getjson(paid_url)
        mids = [ price_or_sentinel(data.get(ticker.upper())) for ticker in tickers]
        return mids


def iex_common_stock_with_balance_sheet_tickers(api_key:str, return_tickers=True, tickers=None, threshold=3000000)->[float]:
    """
        return_tickers: bool   If True, returns list of tickers. If False, returns list of common stock counts
    """
    if tickers is None:
        tickers = iex_common_stock_tickers(api_key=api_key)

    prices = iex_latest_prices(tickers=tickers,api_key=api_key)

    import time
    common = list()
    missing = list()
    small = list()
    for ticker_no, (ticker, price) in enumerate(zip(tickers,prices)):
        paid_url = 'https://cloud.iexapis.com/v1/stock/'+ticker+'/balance-sheet?token=' + api_key
        data = getjson(paid_url, paid_url)
        try:
            cm = data['balancesheet'][0]['commonStock']
            value = float(cm)*float(price)
            if value>threshold:
                if return_tickers:
                    common.append(ticker)
                else:
                    common.append(cm)
            else:
                small.append(ticker)
        except:
            if return_tickers:
                missing.append(ticker)
            else:
                missing.append(ticker)
                common.append(0)

        time.sleep(0.1)
        if ticker_no % 50 == 0:
            print(ticker_no)
            print('There are '+str(len(missing))+' stocks missing balance sheet information ')
            print('There are ' + str(len(common)) + ' stocks with balance sheet that are not too small ')
            print('There are ' + str(len(small)) + ' stocks considered too small ')

    return common


if __name__=='__main__':
    from microprediction.config_private import IEX_KEY
    tickers = ["aapl","abbv","amzn","bac"]
    print(iex_common_stock_with_balance_sheet_tickers(tickers=['googl'], api_key=IEX_KEY))