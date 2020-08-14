from microprediction.writer import MicroWriter
from microprediction.set_config import MICRO_TEST_CONFIG
TEST_WRITE_KEY = MICRO_TEST_CONFIG['TEST_WRITE_KEY']
BASE_URLS = MICRO_TEST_CONFIG['BASE_URLS'][:2]
import time

def test_get_perf():
    for base_url in BASE_URLS:
        mw = MicroWriter(write_key=TEST_WRITE_KEY,base_url=base_url)
        perf = mw.get_performance()
        if not len(perf) >=1 and (time.time()-1597367247)>10*60:
            assert False
