from getjson import mgetjson
from scipy.optimize import newton
import time

# IEX stock prices
# You can get your api_key at https://iexcloud.io/
# See https://iexcloud.io/docs/api/#quote

def force(x, x1, x2, m1, m2, expon=2):
    return m1 / (abs(x - x1) ** expon) - m2 / (abs(x - x2) ** 2)


def weighted_mid(x1, x2, m1, m2, expon=2):
    if x1 >= x2:
        return x1
    else:
        x_mid = 0.5*x1+0.5*x2
        x_weighted = x1 + m1/(m1+m2)**2 * (x2-x1)
        x_guess = 0.25*x_weighted+0.75*x_mid
        try:
            return newton(func=force, x0=x_guess, x1=x_mid, args=(x1, x2, m1, m2, expon), tol=(x2-x1)/100.0 )
        except:
            return x_guess


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


def iex_weighted_mid_prices(tickers, api_key: str, use_free_api=False) -> [float]:
    """
        Asynchronously grab multiple stock prices
    """
    PAID_URL = 'https://cloud.iexapis.com/stable/stock/TICKER/quote?token=YOUR_TOKEN_HERE'
    FREE_URL = 'https://cloud.iexapis.com/stable/tops?token=YOUR_TOKEN_HERE&symbols=TICKER'
    URL = FREE_URL if use_free_api else PAID_URL
    price_urls = [URL.replace('YOUR_TOKEN_HERE', api_key).replace('TICKER', ticker) for ticker in tickers]
    d = mgetjson(urls=price_urls)
    mids = [iex_weighted_mid(di, expon=-1.5) for di in d]
    return mids


def iex_latest_prices(tickers, api_key:str)->[float]:
    """
        Asynchronously grab multiple stock prices
    """
    PAID_URL = 'https://cloud.iexapis.com/stable/stock/TICKER/quote?token=YOUR_TOKEN_HERE'
    price_urls = [PAID_URL.replace('YOUR_TOKEN_HERE', api_key).replace('TICKER', ticker) for ticker in tickers]
    d = mgetjson(urls=price_urls)
    mids = [ di['latestPrice'] for di in d ]
    return mids


if __name__ == '__main__':
    from microprediction.config_private import IEX_KEY
    for _ in range(200):
        time.sleep(1)
        print(iex_latest_prices(tickers=['googl'], api_key=IEX_KEY))


