try:
  from credentials import FATHOM_GAZELLE 
except ImportError:
  raise('This example is not intended to be run. Obtain your own write_key https://www.microprediction.com/private-keys ')

  
# Example illustrating the use of MultiChangePoll 
# This script polls crypto streams and publishes some hypothetical portfolio returns
# It also publishes the square of the returns 
  
from microprediction.polling import MultiChangePoll
from pprint import pprint
from microprediction import MicroWriter
import numpy as np
import math

# Produces conditional realized variance
# Produced conditional returns

COINS = 'bitcoin,ethereum'
C2_NAMES = [ 'c2_'+name+'.json' for name in COINS.split(',') ]

mw = MicroWriter(write_key=FATHOM_GAZELLE)

WEIGHTS = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]

#### Portfolio returns

def portfolio_names():
    return ['portfolio_c2_'+str(W)+'.json' for W in WEIGHTS ]

def portfolio_func(changes):
    values = list()
    for W in WEIGHTS:
        w0 = W/100.
        w1 = 1.0-w0
        change = 1000.*math.log( w0*math.exp(changes[0]/1000.) + w1*math.exp(changes[1]/1000.) )
        values.append(change)
    return values

# Quadratic variation in log(prices)

def quadratic_func(changes):
    dx = np.array([ changes ] )
    dxx = np.matmul(np.transpose(dx),dx)
    print(dxx)
    n_dim = len(C2_NAMES)
    values = list()
    for i in range(n_dim):
        for j in range(i+1,n_dim):
            values.append(dxx[i,j])
    return values

def quadratic_names():
    names = list()
    n_dim = len(C2_NAMES)
    for i in range(n_dim):
        for j in range(i+1,n_dim):
            names.append('quadratic_c2_'+C2_NAMES[i]+'_'+C2_NAMES[j]+'.json')
    return names


def func():
    """ Returns portfolio returns """
    lagged_values = [ mw.get_lagged_values(name=name)[:2] for name in C2_NAMES ]
    print(lagged_values)
    if len(lagged_values[0])>=2:
        changes = [ lv[0]-lv[1] for lv in lagged_values ]
        return list( quadratic_func(changes) ) + list( portfolio_func(changes) )


if __name__=="__main__":
    print('testing',flush=True)
    names = quadratic_names() + portfolio_names()
    pprint(list(zip(names,func())))
    print('starting',flush=True)
    poll = MultiChangePoll(write_key=FATHOM_GAZELLE,func=func,names=names,interval=5,with_copulas=False, verbose=True)
    poll.run()
