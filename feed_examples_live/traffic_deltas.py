#!/usr/bin/python3.8
import requests, datetime
from contexttimer import Timer
from microprediction import MicroWriter
from microprediction.live import bronx_speed
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime


#    Illustrates predicting the change in a quantity when feed is not entirely reliable
#    Here we use the MicroWriter to task people with predicting the change in traffic
#    speed on the Verrazano Bridge every five minutes. However if we don't get good
#    data from the feed or it appears to be stale, we don't send the delta.


try:
    from microprediction.config_private import TRAFFIC_WRITE_KEY
    mw = MicroWriter(write_key=TRAFFIC_WRITE_KEY)
except:
    raise Exception("You need to set the write key for this example to work")

feed_state = "cold"
prev_speed = None
speed = None
NAME  = "bronx_traffic_speed_delta.json"

def fetch_and_send():
    """ Modify feed of speed changes - or at least keep it warm """
    global feed_state, prev_speed, speed

    if feed_state== "warm":
        # A warm state means that previous speed exists and is not stale
        assert prev_speed is not None
        speed = bronx_speed()
        if speed is None:
            feed_state= "cold"
            alert()
            mw.touch(name=NAME)
        else:
            speed = float(speed)
            speed_change = float(speed)-float(prev_speed)
            if abs(speed_change)<1e-5:
                feed_state= "cold"  # Feed is stale, don't judge
                print("****  Feed unchanged at " + str(datetime.datetime.now()),flush=True)
            else:
                with Timer() as t_put:
                    mw.set(name=NAME,value=speed_change)
                    print("Sending speed change "+str(speed_change)+" at "+str(datetime.datetime.now()),flush=True)
                print(str(t_put.elapsed)+ 's putting data.',flush=True)
                prev_speed = speed

    elif feed_state== "cold":
        # Wait until feed is back up and speeds start changing
        prev_prev   = prev_speed if prev_speed else None
        prev_speed  = bronx_speed()
        if (prev_speed is not None) and (prev_prev is not None) and abs(float(prev_prev)-float(prev_speed))>1e-5:
            feed_state= "warm"
            print("**** Feed resumed at " + str(datetime.datetime.now()),flush=True)
        else:
            mw.touch(name=NAME)
            print("Touch at " +str(datetime.datetime.now())+ " - speed is "+str(prev_speed),flush=True )


def alert():
    print("""Something amiss with feed """,flush=True)

#-----------------------------------------------------------------------------------------
#       3. Scheduler
#------------------------------------------------------------------------------------------


def run():
    print('Starting scheduler',flush=True)
    scheduler = BlockingScheduler()
    scheduler.add_job(fetch_and_send, 'interval', minutes=15)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    print('Stopping scheduler',flush=True)

if __name__=="__main__":
    run()


