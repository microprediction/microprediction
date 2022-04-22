
from microprediction.live.xraytickers import get_xray_tickers
from microprediction.live.iex import iex_latest_prices
import math


def get_xray_prices():
    """  Polling function
         Retrieve live prices for the tickers in the xray list
         api_key: An IEX api key
    """
    from microprediction.live.iexcredentials import get_iex_key
    IEX_KEY = get_iex_key()
    tickers = get_xray_tickers()
    sp = iex_latest_prices(tickers=tickers, api_key=IEX_KEY)
    return [1000 * math.log(v) for v in sp]