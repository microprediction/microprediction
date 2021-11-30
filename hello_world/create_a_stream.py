import pandas as pd
from microprediction import MicroWriter

# Video explanation of this example at  https://vimeo.com/443203883
# Video tutorials are available at https://www.microprediction.com/python-1 too


def the_number_you_want_predicted()->float:
    """
       Just an example of polling a live number
       Put your own logic here
    """
    df = pd.read_csv('https://www.ndbc.noaa.gov/data/realtime2/21413.dart')
    return float(df.iloc[1, :].values[0].split(' ')[-1])


if __name__=='__main__':

    # You need a write key
    WRITE_KEY='your key here'
    if WRITE_KEY=='your key here':
        from microconventions import new_key
        print('As you did not supply a key this will burn a new one ... go have a coffee')
        WRITE_KEY = new_key(difficulty=12)

    STREAM_NAME = 'your stream name here.json'
    if STREAM_NAME=='your stream name here.json':
        raise ValueError('Change the stream name')

    # Rest is easy
    mw = MicroWriter(write_key=WRITE_KEY)
    mw.set(name=STREAM_NAME, value=the_number_you_want_predicted())
