from microprediction import new_key, MicroWriter
import numpy as np
try:
    from microprediction.config_private import DODDLE_MAMMAL
except:
    DOODLE_MAMMAL=None

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
        assert saved_back==saved_url

