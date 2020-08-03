from credentials import ELFEST_BOBCAT  # You'll have to supply your own
import pandas as pd
from microprediction import MicroWriter
import time

# Video explanation of this example:
# https://vimeo.com/443203883

mw = MicroWriter(write_key=ELFEST_BOBCAT) # See creating_a_key.py
STREAM_NAME = 'water.json'


def water_height():
    df = pd.read_csv('https://www.ndbc.noaa.gov/data/realtime2/21413.dart')
    return float(df.iloc[1, :].values[0].split(' ')[-1])


def poll_for_an_hour():
    for _ in range(4):
        mw.set(name=STREAM_NAME, value=water_height())
        time.sleep(15 * 60)
        print('.', flush=True)


if __name__ == '__main__':
    poll_for_an_hour()