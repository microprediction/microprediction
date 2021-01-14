# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started creating streams (see the 4th module in particular)

import logging
import urllib
import time
import pytz
import random
from datetime import datetime
from pprint import  pprint
from microprediction import MicroWriter
import os

write_key = os.environ.get('WRITE_KEY')    # GitHub action needs to set env variable. You need to create a GitHub secret called WRITE_KEY
mw = MicroWriter(write_key=write_key)
assert mw.key_difficulty(mw.write_key)>=13, "You need a key of difficulty 13 for copula streams"

NAME_SPEED = 'wind_seatle_speed.json'
NAME_DIR   = 'wind_seatle_direction.json'

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

prev_data = None
idx = None

def fetch_live_data():
    global prev_data
    global idx
    while True:
        try:
            file = urllib.request.urlopen("https://www.ndbc.noaa.gov/data/5day2/WPOW1_5day.cwind")
            if file.status==200:
                # NOTE: file is not indexable
                for i, line in enumerate(file):
                    # most recent data is at line number 3 in the file
                    if i == 2:
                        data = line.decode("utf-8").split()
                        if prev_data == data:
                            idx -= 2
                        else:
                            prev_data = data
                            idx = 6
                        break
                for i, line in enumerate(file):
                    if i == idx:
                        direction = float(data[5]) / 360        # normalize between [0, 1)
                        speed = float(data[6]) / 10             # attempt to normalize
                        return speed, direction
        except:
            logger.error("Connection error: reconnecting...")
            time.sleep(next(wait_time))
    return speed, direction



if __name__=='__main__':
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
    speed, direction = fetch_live_data()
    res = mw.cset(names=[NAME_SPEED, NAME_DIR],values=[speed, direction])
    pprint({'PST time':pst_now.strftime("%H:%M"),'speed':speed,'direction':direction,"res":res})
    print('',flush=True)