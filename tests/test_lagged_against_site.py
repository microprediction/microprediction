from microprediction.writer import MicroReader
from microprediction.set_config import MICRO_TEST_CONFIG
TEST_WRITE_KEY = MICRO_TEST_CONFIG['TEST_WRITE_KEY']
BASE_URLS = MICRO_TEST_CONFIG['BASE_URLS'][1:2]


def test_lagged_20():
    mw = MicroReader(base_url='https://devapi.microprediction.org')
    lagged = mw.get_lagged(name='die.json',count=20)
    assert len(lagged)==20


def test_lagged_2000():
    mw = MicroReader(base_url='https://devapi.microprediction.org')
    lagged = mw.get_lagged(name='die.json',count=2000)
    assert len(lagged)>=1200


