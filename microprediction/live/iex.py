
import time

# IEX stock prices
# You can get your api_key at https://iexcloud.io/
# See https://iexcloud.io/docs/api/#quote



    
  
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


