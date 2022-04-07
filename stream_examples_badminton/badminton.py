from getjson import getjson
try:
    from credentials import DOOMSDAY_STOAT as WRITE_KEY
except ImportError:
    raise EnvironmentError('You need a WRITE_KEY. See https://www.microprediction.com/private-k')
from microprediction import MicroWriter
import time

# Example of creating two streams and a corresponding z2 stream
# This uses cset so you'll need a WRITE_KEY of strength 13


ORIGIN       = 649359149
INTERVAL     = 1          # Minutes between data points
num_digits = len('000000000003')

mw = MicroWriter(write_key=WRITE_KEY)
NAMES = ['badminton_x.json', 'badminton_y.json']

def get_frame_k_data(k):
    TEMPLATE_URL = "https://raw.githubusercontent.com/microprediction/badminton/master/data/game/68mins_640x360_FRAME_keypoints.json"
    url = TEMPLATE_URL.replace('FRAME',str(k).zfill(num_digits))
    data = getjson(url=url)
    if data is not None:
        person = data['people'][0]
        values = [0.01*(v-200) for v in person['pose_keypoints_2d'][3:5]]
        return k, values
    else:
        k+1, None


if __name__=='__main__':
    # Manually loop over cached data

    print(' ')
    print('Restarting',flush=True)
    time.sleep(60*5)
    st = time.time()
    k = 0
    while True:
        v = None
        while v is None:
           k, v = get_frame_k_data(k=k)
           time.sleep(5)
        k = (k+100) % 100000
        print(v)
        mw.cset(names=NAMES,values=v)
        et = time.time()
        wait_time = (st-et) % (INTERVAL*60)
        print('Sleeping for '+str(wait_time))
        time.sleep(wait_time)
