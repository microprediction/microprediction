import math
from microprediction.live.iex import iex_latest_prices


GRAIN_TICKERS = ['weat', 'corn', 'soyb']
GRAIN_NAMES = ['grains_' + ticker + '.json' for k,ticker in enumerate(GRAIN_TICKERS)]


def iex_scaled_log_grains(api_key:str):
    """
       Retrieve live prices for FAANG and transform
       api_key: An IEX api key
    """
    sp = iex_latest_prices(tickers=GRAIN_TICKERS, api_key=api_key)
    return [1000 * math.log(v) for v in sp]

