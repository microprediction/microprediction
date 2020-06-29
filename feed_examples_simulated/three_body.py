#!/usr/bin/python3.8
from microprediction import MicroWriter
from apscheduler.schedulers.blocking import BlockingScheduler
import numpy as np
from pprint import pprint
from scipy.integrate import odeint
from math import sqrt

#  Example of sending live data to www.microprediction.org and kick-starting copula streams
#  This uses the MicroWriter directly, though soon there will be a parent class that makes this more convenient

NAMES = ['three_body_x.json','three_body_y.json','three_body_z.json']
try:
    from microprediction.config_private import THREE_BODY_WRITE_KEY
    mw = MicroWriter(write_key=THREE_BODY_WRITE_KEY)
except:
    raise Exception("You need to set the write key for this example to work, and it must be 'copula strength' ")

SCALE = 10**8
Y0  = [384.6 * 10 ** 6, 0, 0, 1197000, -9928000, 0, 0, 1025, 0, 8490, -2455, 100]
print("Initial value is " + str( [y/SCALE for y in Y0[:3] ]), flush=True)
Y   = Y0



def threebody(Y,t):
    """
       Forked from https://guillaumecantin.pythonanywhere.com/animation/4/
    """
    m1 = 5.974 * 10 ** 24  # Earth
    m2 = 7.348 * 10 ** 22  # Moon
    m3 = 10000            # Spaceship
    g = 6.672 * 10 ** (-10)  # gravitational constant .. should be -11

    def r(x, y, z):
        return sqrt(x * x + y * y + z * z)

    def f(x, y, b, c, d1, d2, d3):
        return -g * (m1 + b) * x / (d1 ** 3) + g * c * ((y - x) / (d2 ** 3) - y / (d3 ** 3))

    dY = [0 for i in range(12)]
    dY[0] = Y[6]
    dY[1] = Y[7]
    dY[2] = Y[8]
    dY[3] = Y[9]
    dY[4] = Y[10]
    dY[5] = Y[11]
    r12 = r(Y[0], Y[1], Y[2])
    r23 = r(Y[0] - Y[3], Y[1] - Y[4], Y[2] - Y[5])
    r13 = r(Y[3], Y[4], Y[5])
    dY[6] = f(Y[0], Y[3], m2, m3, r12, r23, r13)
    dY[7] = f(Y[1], Y[4], m2, m3, r12, r23, r13)
    dY[8] = f(Y[2], Y[5], m2, m3, r12, r23, r13)
    dY[9] = f(Y[3], Y[0], m3, m2, r13, r23, r12)
    dY[10] = f(Y[4], Y[1], m3, m2, r13, r23, r12)
    dY[11] = f(Y[5], Y[2], m3, m2, r13, r23, r12)
    return dY


def evolve():
    global Y
    time = np.arange(0, 0.02*265600, 1)
    orbit = odeint(threebody, Y, time)
    x, y, z, a, b, c, dx, dy, dz, da, db, dc = orbit.T
    values = [ x[-1]/SCALE, y[-1]/SCALE, z[-1]/SCALE ]
    noise  = [ 0.1*np.random.randn() for v in values ]
    noisy_values = [ v + n for v,n in zip(values,noise ) ]
    res = mw.cset(names=NAMES, values=noisy_values)

def demo():
    try:
       import matplotlib.pyplot as plt
    except:
        raise Exception('Need to pip install matplotlib first')
    Y0 = [384.6 * 10 ** 6, 0, 0, 1197000, -9928000, 0, 0, 1025, 0, 8490, -2455, 100]
    time = np.arange(0, 265600, 1)  # 3 days
    orbit = odeint(threebody, Y0, time)
    x, y, z, a, b, c, dx, dy, dz, da, db, dc = orbit.T

    plt.plot(x)
    plt.plot(y)
    plt.show()
    pprint(x)
    pprint(y)
    pprint(z)

def run():

    evolve()

    print('Starting scheduler',flush=True)
    scheduler = BlockingScheduler()
    scheduler.add_job(evolve, 'interval', minutes=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    print('Stopping scheduler',flush=True)


if __name__=="__main__":
    #demo()
    run()




