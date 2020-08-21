from microprediction.config_private import DODDLE_MAMMAL
from microprediction import MicroWriter
import time
from pprint import pprint
import numpy as np

# This example illustrates how easy it is to enter z1~ streams
# For a video explanation of z1 streams and see https://www.linkedin.com/feed/update/urn:li:activity:6696569137365430272/
# See https://www.linkedin.com/pulse/short-introduction-z-streams-peter-cotton-phd/ for an explanation of z-streams.

# You need to set a write key.
# Supplying a URL to your repository is optional.
# This will do is make your position on the leaderboards clickable and direct people to your work.
# You can alternatively provide your personal homepage or LinkedIn profile

WRITE_KEY = DODDLE_MAMMAL
ANIMAL = MicroWriter.animal_from_key(DODDLE_MAMMAL)
REPO = 'https://github.com/microprediction/microprediction/blob/master/crawler_alternatives/' + ANIMAL.lower().replace(
    ' ', '_') + '.py'


# We simply loop over all z1~ streams
# These streams are approximately normally distributed.
# We enter N(0,1) distributed samples so as to try to take advantage of algorithms
# which accidentally submit distributional predictions far from this.
# This code could be run as a cron job or scheduled task at PythonAnywhere, for example

def jiggle():
    return 0.001 * np.random.randn()


if __name__ == "__main__":
    mw = MicroWriter(write_key=WRITE_KEY)
    for name in mw.get_streams():
        if 'z1~' in name:
            values = [mw.norminv(p) + jiggle() for p in mw.percentiles()]
            for delay in mw.DELAYS:
                pprint(mw.submit(name=name, values=values, delay=delay))
                time.sleep(7.28) # No need to overwhelm server
                print('Submitted to '+name+' '+str(delay), flush=True)
