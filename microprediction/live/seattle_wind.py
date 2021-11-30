# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started creating streams (see the 4th module in particular)

import logging
import requests
import urllib
import time
import pytz
import random
from datetime import datetime
from pprint import  pprint
from microprediction import MicroWriter
from microprediction.config_private import TRAFFIC_WRITE_KEY_13
from apscheduler.schedulers.blocking import BlockingScheduler


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def wait_between_attempts():
    """ Incremental backoff between connection attempts """
    wait_time = 19.3  # time is in seconds
    while True:
        yield wait_time
        wait_time = min(wait_time * 1.5, 30)
        wait_time *= (100 + random.randint(0, 50)) / 100

wait_time = wait_between_attempts()


def fetch_live_data():
    while True:
        try:
            file = urllib.request.urlopen("https://www.ndbc.noaa.gov/data/realtime2/WPOW1.cwind")
            if file.status==200:
                # NOTE: file is not indexable
                for i, line in enumerate(file):
                    # most recent data is at line number 3 in the file
                    if i == 2:
                        data = line.decode_meme_stock("utf-8").split()
                        direction = float(data[5]) / 360        # normalize between [0, 1)
                        speed = float(data[6]) / 10             # attempt to normalize
                        return speed, direction
        except:
            logger.error("Connection error: reconnecting...")
            time.sleep(next(wait_time))
    return speed, direction


NAME_SPEED = 'seattle_wind_speed.json'
NAME_DIR   = 'seattle_wind_direction.json'

initial_speed, initial_dir = fetch_live_data()
print("Initial speed is " + str(initial_speed) + " m/s and initial direction is " + str(initial_dir), flush=True)

try:
    mw = MicroWriter(write_key=TRAFFIC_WRITE_KEY_13)
except:
    raise Exception("You need to set the write key for this example to work")


def poll_and_send():
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
    speed, direction = fetch_live_data()
    res = mw.cset(names=[NAME_SPEED, NAME_DIR],values=[speed, direction])
    pprint({'PST time':pst_now.strftime("%H:%M"),'speed':speed,'direction':direction,"res":res})
    print('',flush=True)

def run():
    print('Starting scheduler',flush=True)
    scheduler = BlockingScheduler()
    scheduler.add_job(poll_and_send, 'interval', minutes=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    print('Stopping scheduler',flush=True)


if __name__=="__main__":
    run()
