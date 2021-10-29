from microprediction.writer import MicroWriter
from microprediction.set_config import MICRO_TEST_CONFIG

BASE_URLS = MICRO_TEST_CONFIG['BASE_URLS']


def test_get_predictions_ethereum():
    for base_url in [ BASE_URLS[1] ]:  # devapi only
        mw = MicroWriter(write_key=MICRO_TEST_CONFIG['EMBLOSSOM_MOTH'],base_url=base_url)
        name = 'c5_ethereum'
        delay = 3555
        tickets = mw.get_own_predictions(name=name,delay=delay,strip=False)
        assert isinstance(tickets,dict)
        preds = mw.get_own_predictions(name=name,delay=delay,strip=True,consolidate=False)
        assert isinstance(preds, list)
        assert isinstance(preds[0], tuple)
        values = mw.get_own_predictions(name=name, delay=delay, strip=True, consolidate=True)
        assert isinstance(values,list)



