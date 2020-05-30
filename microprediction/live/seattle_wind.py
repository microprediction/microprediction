import logging
import requests
import time
import pytz
import random
from datetime import datetime
from pprint import  pprint

from microprediction import MicroWriter
from microprediction.config_private import TRAFFIC_WRITE_KEY

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


# Average delays for all BART train lines

def fetch_live_data():
    total_delay = 0
    lines = 0
    while True:
        try:
            r = requests.get("https://www.ndbc.noaa.gov/data/realtime2/WPOW1.cwind")
            print(type(r))
            print(r)
            if r.status_code==200:
                station_data = r.json()["root"]["station"]

        except requests.exceptions.RequestException as e:
            logger.error("Connection error %s: reconnecting..." % e)
            time.sleep(next(wait_time))
    return speed, direction


NAME = 'seattle_wind_speed_and_direction.json'

initial_speed, initial_dir = fetch_live_data()
print("Initial speed is " + str(initial_speed) + " and initial direction is " str(initial_dir) + " m/s", flush=True)

try:
    mw = MicroWriter(write_key=TRAFFIC_WRITE_KEY)
except:
    raise Exception("You need to set the write key for this example to work")


def poll_and_send():
    """ Create stream of average delay in seconds """
    speed, direction = all_stations_delay()
    # res = mw.set(name=NAME,value=float(value))
    res = "FIX ME"
    pprint({'PST time':pst_now.strftime("%H:%M"),'speed':speed,'direction':direction,"res":res})
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
