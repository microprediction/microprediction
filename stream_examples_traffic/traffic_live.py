#!/usr/bin/python3.8
from microprediction import MicroWriter
from microprediction.live import bronx_speed
from apscheduler.schedulers.blocking import BlockingScheduler
from pprint import  pprint
import datetime

#  Example of sending live data to www.microprediction.com
#  Data server is really slow

NAME = 'bronx_traffic_absolute_speed.json'

# Let's fail fast
initial_value = float(bronx_speed())
print("Initial value is " + str(initial_value), flush=True)


try:
    from microprediction.config_private import TRAFFIC_WRITE_KEY
    mw = MicroWriter(write_key=TRAFFIC_WRITE_KEY)
except:
    raise Exception("You need to set the write key for this example to work")

def poll_and_send():
    """ Create stream of traffic speed """
    value = bronx_speed()
    res = mw.set(name=NAME,value=float(value))
    pprint({'speed':value,"res":res})
    print('',flush=True)

def run():
    print('Starting scheduler',flush=True)
    scheduler = BlockingScheduler()
    scheduler.add_job(poll_and_send, 'interval', minutes=20)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    print('Stopping scheduler',flush=True)

if __name__=="__main__":
    run()


