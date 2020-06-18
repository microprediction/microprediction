from getjson import getjson
import time

def test_getjson():
    start_time = time.time()
    for k in range(5):
        getjson('https://config.microprediction.org/config.json')
    end_time = time.time()
    assert end_time-start_time<5