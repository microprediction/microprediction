import logging
import requests
import time
import pytz
import random
from datetime import datetime
from pprint import  pprint

from microprediction import MicroWriter
try:
    from microprediction.config_private import TRAFFIC_WRITE_KEY, BART_KEY
except:
    print("This won't run without creds")

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

def fetch_live_data(station):
    """ Given specific station (or "ALL") as input, returns the average delay in seconds """
    total_delay = 0
    lines = 0
    while True:
        try:
            r = requests.get("http://api.bart.gov/api/etd.aspx?cmd=etd&orig="+station+"&key="+BART_KEY+"&json=y")
            if r.status_code==200:
                station_data = r.json()["root"]["station"]
                for station in station_data:
                    for destination in station["etd"]:
                        if len(destination["estimate"]) != 0:
                            total_delay += int(destination["estimate"][0]["delay"])
                            lines += 1
                # fail-safe for wide BART shutdowns. On average ~180 lines
                return float(total_delay) / lines if lines > 15 else None
        except requests.exceptions.RequestException as e:
            logger.error("Connection error %s: reconnecting..." % e)
            time.sleep(next(wait_time))
    return float(total_delay) / lines if lines > 15 else None

def all_stations_delay():
    return fetch_live_data(station="ALL")



NAME = 'bart_delays.json'

initial_value = all_stations_delay()
print("Initial value is " + str(initial_value) + " seconds", flush=True)

try:
    mw = MicroWriter(write_key=TRAFFIC_WRITE_KEY)
except:
    raise Exception("You need to set the write key for this example to work")


def poll_and_send():
    """ Create stream of average delay in seconds """

    # avoid publishing during BART's off-hours
    # NOTE: these are COVID-specific hours; adjust later
    # weekday hours: 5am-9pm
    # weekend hours: 8am-9pm
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
    if pst_now.weekday() <= 4 and (pst_now.hour < 5 or pst_now.hour >= 21) \
    or pst_now.weekday() >= 5 and (pst_now.hour < 8 or pst_now.hour >= 21):
        print("{}: Off-Hours".format(pst_now.strftime("%H:%M")))
        return

    value = all_stations_delay()
    if value is None:
        print("{}: <= 15 Lines but On-Hours".format(pst_now.strftime("%H:%M")))
    else:
        res = mw.set(name=NAME,value=float(value))
        pprint({'PST time':pst_now.strftime("%H:%M"),'average delay':value,"res":res})
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
