# IEX stock prices
# You can get your api_key at https://iexcloud.io/
# See https://iexcloud.io/docs/api/#quote


def iex_latest_prices(tickers, api_key:str)->[float]:
    """
        Grab multiple stock prices
    """
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