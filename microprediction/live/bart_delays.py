import requests
import datetime
from pprint import  pprint
from apscheduler.schedulers.blocking import BlockingScheduler

from microprediction import MicroWriter
from microprediction.config_private import TRAFFIC_WRITE_KEY, BART_KEY

# Average delays for all BART train lines

def fetch_live_data(station):
    """ Given specific station (or "ALL") as input, returns the average delay in seconds """
    total_delay = 0
    lines = 0
    r = requests.get("http://api.bart.gov/api/etd.aspx?cmd=etd&orig="+station+"&key="+BART_KEY+"&json=y")
    if r.status_code==200:
        station_data = r.json()["root"]["station"]
        for station in station_data:
            for destination in station["etd"]:
                if len(destination["estimate"]) is not 0:
                    total_delay += int(destination["estimate"][0]["delay"])
                lines += 1
        return float(total_delay) / lines
    else:
        return None

def all_stations_delay():
    return fetch_live_data(station="ALL")



NAME = 'bart_delays.json'

initial_value = all_stations_delay()
print("Initial value is " + str(initial_value) + " seconds", flush=True)


def poll_and_send():
    """ Create stream of average delay in seconds """
    value = all_stations_delay()
    # res = mw.set(name=NAME,value=float(value))
    res = 0
    pprint({'average delay':value,"res":res})
    print('',flush=True)

def run():
    try:
        mw = MicroWriter(write_key=TRAFFIC_WRITE_KEY)
    except:
        raise Exception("You need to set the write key for this example to work")
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

