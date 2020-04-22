import logging
import requests
import time
import pytz
import random
from datetime import datetime, timedelta
from pprint import  pprint

from microprediction import MicroWriter
from microprediction.config_private import TRAFFIC_WRITE_KEY


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Number of bikes available near large Manhattan hospitals
# longitude and latitude of rectangles within 500 feet of hospital
# citibike map: https://member.citibikenyc.com/map/
COORDS = [
    ((40.787880, -73.955862), (40.792001, -73.948389)),     # Mount Sinai - station_ids: 3345, 3299, 3363
    ((40.763573, -73.959175), (40.766666, -73.950179)),     # New York Presbytarian Upper East Side - station_ids: 3156, 3141
    ((40.735625, -73.979437), (40.743511, -73.970913)),     # Bellevue and NYU Langone - station_ids: 545, 3687, 174, 528, 536, 2012
    ((40.709229, -74.008624), (40.712033, -74.002787)),     # New York Presbytarian Lower Manhattan - station_ids: 224, 316
    ((40.783116, -73.949118), (40.787085, -73.939771)),     # Metropolitan Hospital Center - station_ids: 3309, 3318, 3338, 3351
]


def wait_between_attempts():
    """ Incremental backoff between connection attempts """
    wait_time = 19.3  # time is in seconds
    while True:
        yield wait_time
        wait_time = min(wait_time * 1.5, 30)
        wait_time *= (100 + random.randint(0, 50)) / 100

wait_time = wait_between_attempts()


def get_station_ids():
    """ Given COORDS, return all station_ids that fall within the rectangles """
    station_ids = []
    while True:
        try:
            r = requests.get("https://feeds.citibikenyc.com/stations/stations.json")
            if r.status_code==200:
                data = r.json()
                for c1, c2 in COORDS:
                    station_data = [ 
                        d for d in data["stationBeanList"] \
                        if d["latitude"] > c1[0] and d["latitude"] < c2[0] \
                        and d["longitude"] > c1[1] and d["longitude"] < c2[1]
                    ]
                    for station in station_data:
                        station_ids.append(int(station["id"]))
                return station_ids
        except requests.exceptions.RequestException as e:
            logger.error("Connection error %s: reconnecting..." % e)
            time.sleep(next(wait_time))
    return station_ids

def fetch_live_data(keys,field):
    """ Given list of station_ids as input, returns list of station[field] """
    while True:
        try:    
            r = requests.get("https://feeds.citibikenyc.com/stations/stations.json")
            if r.status_code==200:
                data = r.json()
                station_data = [ d for d in data["stationBeanList"] if int(d["id"]) in keys ]
                return [ station[field] for station in station_data ]
        except requests.exceptions.RequestException as e:
            logger.error("Connection error %s: reconnecting..." % e)
            time.sleep(next(wait_time))


def hospital_bike_activity(station_ids):
    prev = fetch_live_data(keys=station_ids,field="availableBikes")
    end_time = datetime.now() + timedelta(minutes = 20)
    activity = 0
    # measure activity change every 2 minutes for 20 minutes
    while datetime.now() < end_time:
        time.sleep(2 * 60)
        curr = fetch_live_data(keys=station_ids,field="availableBikes")
        for i in range(len(station_ids)):
            activity += abs(curr[i] - prev[i])
        prev = curr
    return activity



NAME = 'hospital_bike_activity.json'

station_ids = get_station_ids()
print("Initial activity is " + str(0), flush=True)


def run():
    try:
        mw = MicroWriter(write_key=TRAFFIC_WRITE_KEY)
    except:
        raise Exception("You need to set the write key for this example to work")
    while True:
        value = hospital_bike_activity(station_ids)
        utc_now = pytz.utc.localize(datetime.utcnow())
        pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
        res = mw.set(name=NAME,value=float(value))
        pprint({'PST time':pst_now.strftime("%H:%M"),'activity':value,"res":res})
        print('',flush=True)


if __name__=="__main__":
    run()
