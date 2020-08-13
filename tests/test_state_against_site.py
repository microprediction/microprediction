from microprediction.set_config import MICRO_TEST_CONFIG
import random
from microprediction.writer import MicroWriter

# Test MicroWriter state storage capability against www.microprediction.org

TEST_WRITE_KEY = MICRO_TEST_CONFIG['TEST_WRITE_KEY']
BASE_URLS = [MICRO_TEST_CONFIG["base_url"],MICRO_TEST_CONFIG["dev_base_url"]]

TEST_VALUES = [ ('sam',17),{'frogs legs': 11},
                 11,
                 'dog',
                 3.14156,
                 ('sam', {'mary': 11, 'bob': 32})]


def test_state_storage_and_retrieval():
    """ Test on actual redis instance """
    for base_url in BASE_URLS:
        writer = MicroWriter(write_key=TEST_WRITE_KEY,base_url=base_url)
        k = random.choice(list(range(10)))
        for value in TEST_VALUES:
            res1 = writer.set_state(k=k, value=value)
            assert res1['success']
            value_back = writer.get_state(k=k)
            if isinstance(value,(list,dict,str)):
                assert MicroWriter.deep_equal(value, value_back)
            elif isinstance(value, tuple):
                assert MicroWriter.deep_equal(value,tuple(value_back))
            elif isinstance(value, int):
                assert int(value_back) == value
            elif isinstance(value, float):
                assert abs(float(value_back) - value) < 1e-6
