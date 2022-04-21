import math
from microprediction.live.iex import iex_latest_prices
from microprediction.live.xraytickers import XRAY_TICKERS



XRAY_NUM = len(XRAY_TICKERS)
XRAY_NAMES = ['r_' + str(k) + '.json' for k, ticker in enumerate(XRAY_TICKERS)]


def iex_scaled_log_xray(api_key:str):
    """
       Retrieve live prices
       api_key: An IEX api key
    """
    sp = iex_latest_prices(tickers=XRAY_TICKERS, api_key=api_key)
    return [1000 * math.log(v) for v in sp]


if __name__=='__main__':
    print(len(XRAY_NAMES))


