from microprediction.writer import MicroWriter
from microprediction.set_config import MICRO_TEST_CONFIG
TEST_WRITE_KEY = MICRO_TEST_CONFIG['TEST_WRITE_KEY']
BASE_URLS = MICRO_TEST_CONFIG['BASE_URLS'][1:2]


def dont_test_prizes():
    # Won't work until after push
    for base_url in BASE_URLS:
        mw = MicroWriter(write_key=TEST_WRITE_KEY,base_url=base_url)
        prizes = mw.get_prizes()
        assert isinstance(prizes,list)
        assert prizes[0].get('article')
        for prize in prizes:
            leaderboard = mw.get_leaderboard_for_prize(prize=prize)
            assert len(leaderboard)>2


