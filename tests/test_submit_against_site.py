from microprediction.writer import MicroWriter
from microprediction.set_config import MICRO_TEST_CONFIG

BASE_URLS = MICRO_TEST_CONFIG['BASE_URLS']

def test_die_submit():
    for base_url in BASE_URLS:
        mw = MicroWriter(write_key=MICRO_TEST_CONFIG['TEST_WRITE_KEY'],base_url=base_url)
        die_values = [-2.5,-1.5,-0.5,0.5,1.5,2.5]*37+[-2.5,-1.5,2.5]
        for delay in mw.DELAYS:
            assert mw.submit(name='die.json',values=die_values,delay=delay)
