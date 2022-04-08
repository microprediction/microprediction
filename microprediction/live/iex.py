# IEX stock prices
# You can get your api_key at https://iexcloud.io/
# See https://iexcloud.io/docs/api/#quote
from getjson import getjson


def iex_latest_prices(tickers, api_key:str)->[float]:
    """
        Grab multiple stock prices
        IEX allows only 100 at a time
    """
    if len(tickers)>100:
        tickerlists = [tickers[i:i + 100] for i in range(0, len(tickers), 100)]
        mids = [ iex_latest_prices(tickers=ticks, api_key=api_key) for ticks in tickerlists ]
        mids_flat = [item for sublist in mids for item in sublist]
        return mids_flat
    else:
        symbols = ','.join(tickers)
        paid_url = 'https://cloud.iexapis.com/v1/stock/market/batch?types=price&symbols='+symbols+'&token=' + api_key
        print(paid_url)
        data = getjson(paid_url)
        mids = [ data[ticker.upper()]['price'] for ticker in tickers]
        return mids


if __name__ == '__main__':
    from pprint import pprint
    from getjson import getjson
    from microprediction.config_private import IEX_KEY
    tickers = ['aapl','googl']
    data = iex_latest_prices(tickers=tickers, api_key=IEX_KEY)
    pprint(data)