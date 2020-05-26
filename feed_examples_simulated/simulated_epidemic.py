#!/usr/bin/python3.8
from microprediction import MicroWriter
from apscheduler.schedulers.blocking import BlockingScheduler
import numpy as np
from pprint import pprint
from scipy.integrate import odeint, solve_ivp
import math


#
#   Work in progress ... broken currently
#


#  Example of sending live data to www.microprediction.com to predict a simulated sequence
#  We generate a time series of the number of people who are infected in a model for an epidemic
#  that is similar to CIR but takes novelty of interaction into account. see https://www.overleaf.com/read/sgjvfxydcwpk
#  The time series comprises a sequence of daily observations (real time) updated every 90 seconds.

NAMES = ['susceptible','infected','recovered']
DT    = 90                # Seconds between each update

try:
    from microprediction.config_private import MATCHABLE_BAT
    mw = MicroWriter(write_key=MATCHABLE_BAT)
except:
    raise Exception("You need to set the write key for this example to work, and it must be 'copula strength' ")


def entire(a,t):
    if a*t>1e-4:
        return ( 1-math.exp(-a*t))/(a*t)
    else:
        return 1.0


def compartmental(t,y,a,b,gamm):
    """
       Augmented CIR model
         ds = - beta(t) s i
         di = beta(t) s i - gamma i
         dr = gamma i
         where beta(t) = beta (1-exp(-alpha*t))/(alpha*t)
    """
    beta_ = b*entire(a=a,t=t)
    return [ -beta_*y[0]*y[1], beta_*y[0]*y[1] - gamm*y[1], gamm*y[1] ]

def demo():
    try:
       import matplotlib.pyplot as plt
    except:
        raise Exception('Need to pip install matplotlib first')

    # Initial conditions
    i0 = 0.01
    y0 = [1-i0,i0,0]
    alph = 0.005
    beta  = 0.1
    gamm = 0.05

    T = 150

    # Evolve DEs
    evolver = lambda t,y: compartmental(t=t,y=y,a=alph,b=beta,gamm=gamm)
    sol = solve_ivp(evolver, t_span=[0,T], y0=y0, dense_output=True )
    t = np.linspace(0,T,2*T)
    z = sol.sol(t)
    plt.plot(t,z.T)
    plt.legend(['Susceptible','Infected','Recovered'])
    #plt.yscale('log')
    plt.show()


def feed():
    pass

def run():

    print('Starting scheduler',flush=True)
    scheduler = BlockingScheduler()
    scheduler.add_job(feed, 'interval', minutes=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    print('Stopping scheduler',flush=True)


if __name__=="__main__":
    demo()
    run()




