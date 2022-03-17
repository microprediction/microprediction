from microprediction.config_private import LEGLESS_OCELOT as WRITE_KEY
from microprediction.config_private import IEX_KEY
from microprediction.polling import MultiChangePoll
from microprediction.live.iex import iex_realtime_prices
import math

# Simple example of publishing changes in log prices

FAANG = ['fb','aapl','amzn','nflx','googl']


def scaled_log_faang():
    sp = iex_realtime_prices(tickers=FAANG, api_key=IEX_KEY)
    return [1000 * math.log(v) for v in sp]


if __name__=='__main__':
    faang_names = [ 'faang_'+ticker+'.json' for ticker in FAANG ]
    mcp = MultiChangePoll(write_key=WRITE_KEY, names = faang_names, interval=5, func=scaled_log_faang, with_copulas=False)
    mcp.set_repository('https://github.com/microprediction/microprediction/tree/master/stream_examples_stocks')
    mcp.run()
