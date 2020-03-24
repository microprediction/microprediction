#!/usr/bin/python3.8
from microprediction import MicroWriter
from microprediction.live import bronx_speed
from apscheduler.schedulers.blocking import BlockingScheduler
from pprint import  pprint
import datetime

#  Example of sending live data change to www.microprediction.com

try:
    from microprediction.config_private import TRAFFIC_WRITE_KEY
    mw = MicroWriter(write_key=TRAFFIC_WRITE_KEY)
except:
    raise Exception("You need to set the write key for this example to work")

NAME  = "bronx_traffic_speed_on_change.json"

prev_speed = None

def poll_and_send_if_changed():
    """ Modify feed of speed changes - or at least keep it warm """
    global speed, prev_speed

    if prev_speed is None:
        prev_speed = bronx_speed()
        speed      = None
    else:
        speed = bronx_speed()
        try:
            fspeed = float(speed)
            fprev  = float(prev_speed)
            if abs(fspeed-fprev)>1e-5:
                print( mw.set(name=NAME,value=fspeed-fprev) )
                prev_speed = speed
            else:
                mw.touch(name=NAME)
        except:
            mw.touch(name=NAME)
        pprint({"time":str(datetime.datetime.now()),"prev_speed":prev_speed,"speed":speed})

def run():
    print('Starting scheduler',flush=True)
    scheduler = BlockingScheduler()
    scheduler.add_job(poll_and_send_if_changed, 'interval', minutes=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    print('Stopping scheduler',flush=True)

if __name__=="__main__":
    run()


