from microprediction.config_private import EMBLOSSOM_MOTH  # Burn your own at MUID.org
from microprediction.polling import MultiChangePoll
from microprediction.live.crypto import names_and_prices
import math

def func():
    """ Example of function returning live data as [ float ]

         :returns  [ float ]     Vector of four coin prices (scaled logarithms of prices)
    """
    names, values = names_and_prices()
    return [ 1000*math.log(v) for v in values ]

NAMES = [name +'.json' for name in names_and_prices()[0]]

if __name__=="__main__":
    poll = MultiChangePoll(write_key=EMBLOSSOM_MOTH,func=func,names=NAMES,interval=3,with_copulas=True, verbose=True)
    poll.run()
