from credentials import HAMOSE_CHEETAH
import logging
import urllib
import time
import random
from microprediction import MicroWriter

mw = MicroWriter(write_key=HAMOSE_CHEETAH)
assert mw.key_difficulty(mw.write_key)>=13, "You need a key of difficulty 13 for copula streams"
mw.set_repository(url='https://github.com/microprediction/microprediction/blob/master/microprediction/live/noaa_wind.py') # courtesy

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def wait_between_attempts():
    """ Incremental backoff between connection attempts """
    wait_time = 5.3  # time is in seconds
    while True:
        yield wait_time
        wait_time = min(wait_time * 1.5, 30)
        wait_time *= (100 + random.randint(0, 50)) / 100

wait_time = wait_between_attempts()

prev_data = None
idx = None


def fetch_live_data(location):
    global prev_data
    global idx
    speed = 0
    direction = 0
    for retry_no in range(3):
        try:
            url = "https://www.ndbc.noaa.gov/data/5day2/"+location+"_5day.cwind"
            print(url)
            file = urllib.request.urlopen(url=url)
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


LOCATIONS_1 = ['41008','44005','46060','46061']
LOCATIONS_2 = ['46073','46076','46077','46078']


def fetch_data(locations):
    names = list()
    values = list()
    for location in locations:
        speed, direction = fetch_live_data(location=location)
        names.append('noaa_wind_speed_'+location+'.json')
        values.append(speed)
        names.append('noaa_wind_direction_'+location+'.json')
        values.append(direction)
    return names, values



if __name__=='__main__':
    for locations in [LOCATIONS_1,LOCATIONS_2]:
        names, values = fetch_data(locations=locations)
        res = mw.cset(names=names, values=values)
