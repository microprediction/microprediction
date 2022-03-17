from getjson import mgetjson


# IEX stock prices
# You can get your api_key at https://iexcloud.io/


def iex_realtime_prices(tickers, api_key:str, use_free_api=False )->[float]:
    """
        Asynchronously grab multiple stock prices
    """
    PAID_URL = 'https://cloud.iexapis.com/stable/stock/TICKER/quote?token=YOUR_TOKEN_HERE'
    FREE_URL = 'https://cloud.iexapis.com/stable/tops?token=YOUR_TOKEN_HERE&symbols=TICKER'
    URL = FREE_URL if use_free_api else PAID_URL
    price_urls =  [ URL.replace('YOUR_TOKEN_HERE',api_key).replace('TICKER',ticker) for ticker in tickers ]
    data = mgetjson(urls=price_urls)
    return [ d['iexRealtimePrice'] for d in data ]


