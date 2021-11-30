from microprediction.config_private import EMBLOSSOM_MOTH  # Burn your own with new_key(difficulty=13)
from microprediction.polling import MultiChangePoll
from pycoingecko import CoinGeckoAPI
import math
from pprint import pprint

# This is the actual code used to generate the copula contests

COINS = 'bitcoin,ethereum,ripple,cardano,iota'
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
    poll = MultiChangePoll(write_key=EMBLOSSOM_MOTH,func=func,names=NAMES,interval=5,with_copulas=True, verbose=True)
    poll.run()
