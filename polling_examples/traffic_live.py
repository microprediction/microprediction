from microprediction.polling import MicroPoll
from microprediction import new_key
from microprediction.live.nyc_traffic import verrazano_speed

try:
    from microprediction.config_private import TRAFFIC_WRITE_KEY
except:
    TRAFFIC_WRITE_KEY = new_key(difficulty=12)  # Could take a while!

if __name__=="__main__":
    feed = MicroPoll(write_key=TRAFFIC_WRITE_KEY,
                     name='verrazano_speed.json',
                     func=verrazano_speed,
                     interval=1)
    feed.run()

