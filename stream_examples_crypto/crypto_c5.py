try:
    from credentials import EMBLOSSOM_MOTH as WRITE_KEY
except ImportError:
    raise('This is just for show, not intended for running')

from microprediction.polling import MultiChangePoll
from pycoingecko import CoinGeckoAPI
import math
from pprint import pprint


COINS = 'bitcoin,ethereum,tether,cardano,solana'
NAMES = [ 'c5_'+name+'.json' for name in COINS.split(',') ]

def func():
    """ Returns five large cap coins in USD """
    cg   = CoinGeckoAPI()
    data = cg.get_price(ids=COINS, vs_currencies='usd')
    pprint(data)
    raw  = [ data[coin]['usd'] for coin in COINS.split(',') ]
    return [ 1000*math.log(v) for v in raw ]


if __name__=="__main__":
    print('testing',flush=True)
    pprint(func())
    print('starting',flush=True)
    poll = MultiChangePoll(write_key=WRITE_KEY,func=func,names=NAMES,interval=15,with_copulas=True, verbose=True)
    poll.run()

