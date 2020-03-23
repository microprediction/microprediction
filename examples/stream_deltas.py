#!/usr/bin/python3.8
import requests, datetime
from contexttimer import Timer
from microprediction import MicroWriter
from apscheduler.schedulers.blocking import BlockingScheduler

try:
    from microprediction.config_private import TRAFFIC_WRITE_KEY
except:
    raise Exception("You need to set the write key for this example to work")

#    Illustrates predicting the change in a quantity when feed is not entirely reliable
#    Here we use the MicroWriter to task people with predicting the change in traffic
#    speed on the Verrazano Bridge every five minutes. However if we don't get good
#    data from the feed or it appears to be stale, we don't send the delta.

#-----------------------------------------------------------------------------------------
#    1. External data fetching
#------------------------------------------------------------------------------------------

URL   = "https://data.cityofnewyork.us/resource/i4gi-tjb9.json"  # MTA city of NY realtime feed
VBID  = "416"  # "Verrazano-Narrows-Bridge"

def fetch_live_data(key,field):
    r = requests.get(URL)
    if r.status_code==200:
        data = r.json()
        selection = [ d for d in data if int(d["id"])==int(key) and d["status"]=="0"]
        selection.sort(key=lambda x:x["data_as_of"], reverse=True)
        if len(selection)>0:
            record = selection[0]
            return record[field]
        else:
            return None
    else:
        return None

def verrazano_speed():
    return fetch_live_data(key=VBID,field="speed")


#-----------------------------------------------------------------------------------------
#       2. Feed monitoring task to be run every minute
#------------------------------------------------------------------------------------------

mw     = MicroWriter(write_key=WRITE_KEY)
NAME   = "verrazano"
feed_state = "cold"
prev_speed = None
speed = None

def fetch_and_send():
    """ Modify feed of speed changes - or at least keep it warm """
    # TODO: Obviate this kind of logic by providing it for the feed provider
    global feed_state, prev_speed, speed

    if feed_state== "warm":
        # A warm state means that previous speed exists and is not stale
        assert prev_speed is not None
        speed = verrazano_speed()
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
        prev_speed  = verrazano_speed()
        if (prev_speed is not None) and (prev_prev is not None) and abs(float(prev_prev)-float(prev_speed))>1e-5:
            feed_state= "warm"
            print("**** Feed resumed at " + str(datetime.datetime.now()),flush=True)
        else:
            mw.touch(name=NAME)
            print("Touch at " +str(datetime.datetime.now())+ " - speed is "+str(prev_speed),flush=True )


def alert():
    print("""
     
        Looks like the feed is ...
                 ,----..                            ,--.
    ,---,       /   /   \             .---.       ,--.'|
  .'  .' `\    /   .     :           /. ./|   ,--,:  : |
,---.'     \  .   /   ;.  \      .--'.  ' ;,`--.'`|  ' :
|   |  .`\  |.   ;   /  ` ;     /__./ \ : ||   :  :  | |
:   : |  '  |;   |  ; \ ; | .--'.  '   \' .:   |   \ | :
|   ' '  ;  :|   :  | ; | '/___/ \ |    ' '|   : '  '; |
'   | ;  .  |.   |  ' ' ' :;   \  \;      :'   ' ;.    ;
|   | :  |  ''   ;  \; /  | \   ;  `      ||   | | \   |
'   : | /  ;  \   \  ',  /   .   \    .\  ;'   : |  ; .'
|   | '` ,/    ;   :    /     \   \   ' \ ||   | '`--'
;   :  .'       \   \ .'       :   '  |--" '   : |
|   ,.'          `---`          \   \ ;    ;   |.'
'---'                            '---"     '---

        Will monitor until it is up again 

""",flush=True)

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
    verrazano_speed()


