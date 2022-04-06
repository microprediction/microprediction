
import time

# IEX stock prices
# You can get your api_key at https://iexcloud.io/
# See https://iexcloud.io/docs/api/#quote


def iex_weighted_mid(d, expon=-1.5):
    x1 = d['iexBidPrice']
    x2 = d['iexAskPrice']
    m1 = d['iexBidSize']
    m2 = d['iexAskSize']
    if (x1 != 0) and (x2 != 0) and (m1 != 0) and (m2 != 0) and (x2 > x1):
        wm = weighted_mid(x1=x1, x2=x2, m1=m1, m2=m2)
        print({'x1': x1, 'm1': m1, 'x2': x2, 'm2': m2, 'wm': wm})
        return wm
    else:
        return d['latestPrice']

    
  
def iex_latest_prices(tickers, api_key:str)->[float]:
    """
        Asynchronously grab multiple stock prices
        (WARNING: grequests is a terrible gremlin that monkey patches requests)
    """
    
    def ggetjson():
        return None
    
    try:
        import grequests
        def ggetjson(urls):
            rs = (grequests.get(u) for u in urls)
            rs_map = grequests.map(rs)
            return [r.json() for r in rs_map]
    except ImportError:
        raise Exception('pip install grequests')
   
    
    PAID_URL = 'https://cloud.iexapis.com/stable/stock/TICKER/quote?token=YOUR_TOKEN_HERE'
    price_urls = [PAID_URL.replace('YOUR_TOKEN_HERE', api_key).replace('TICKER', ticker) for ticker in tickers]
    d = ggetjson(urls=price_urls)
    mids = [ di['latestPrice'] for di in d ]
    return mids


if __name__ == '__main__':
    from microprediction.config_private import IEX_KEY
    for _ in range(200):
        time.sleep(1)
        print(iex_latest_prices(tickers=['googl'], api_key=IEX_KEY))


