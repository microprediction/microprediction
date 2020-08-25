from microprediction import MicroWriter
from microprediction.set_config import MICRO_TEST_CONFIG

DODDLE_MAMMAL = MICRO_TEST_CONFIG['DODDLE_MAMMAL']


def test_repo_live():
    if DODDLE_MAMMAL is not None:
        mw = MicroWriter(write_key=DODDLE_MAMMAL, base_url='https://devapi.microprediction.org')
        saved_url = mw.get_own_repository()
        res = mw.set_repository(url='https://www.linkedin.com/in/petercotton/detail/recent-activity/posts/')
        print(mw.get_own_repository())
        print(res)
        res = mw.delete_repository()
        mw.set_repository(url=saved_url)
        saved_back = mw.get_own_repository()
        assert saved_back == saved_url
