from microprediction.writer import MicroWriter
from microprediction.set_config import MICRO_TEST_CONFIG
TEST_WRITE_KEY = MICRO_TEST_CONFIG['TEST_WRITE_KEY']
BASE_URLS = MICRO_TEST_CONFIG['BASE_URLS'][1:2]


def test_prizes():
    for base_url in BASE_URLS:
        mw = MicroWriter(write_key=TEST_WRITE_KEY,base_url=base_url)
        prizes = mw.get_prizes()
        assert isinstance(prizes,list)
        assert prizes[0].get('article')
        for prize in prizes:
            leaderboard = mw.get_prize_leaderboard(prize_type=prize['type'],sponsor=prize['sponsor'])
            assert len(leaderboard)>2


