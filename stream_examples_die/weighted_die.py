try:
    from microprediction.config_private import DOOMSDAY_STOAT
except ImportError:
    raise EnvironmentError('Not a working example as is. Change to use your own write key.')

from microprediction import MicroWriter
import random

# Illustrates how to publish a value to a stream
# (You might run this every hour, say)

def weighted_die():
    FACES=[1,2,3,4,5,6]
    return random.choices(population=FACES,weights=FACES)[0]


if __name__=='__main__':
    STREAM_NAME = 'die.json'    # <--- Change this too1
    mw = MicroWriter(write_key=DOOMSDAY_STOAT)
    value = weighted_die()
    res = mw.set(name='die.json', value=value)
    print(res)