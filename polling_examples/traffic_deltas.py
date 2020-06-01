# Reimplementation of feed_examples_live/traffic_deltas using scheduler

from microprediction.polling import ChangePoll
from microprediction import new_key
from microprediction.live import verrazano_speed

try:
    from microprediction.config_private import TRAFFIC_WRITE_KEY
except:
    TRAFFIC_WRITE_KEY = new_key(difficulty=12)  # Could take a while!

if __name__=="__main__":
    changes = ChangePoll(write_key=TRAFFIC_WRITE_KEY,
                        name='verrazano_speed_change.json',
                    interval=1,
                    func=verrazano_speed)
    changes.run()


