from microprediction.writer import MicroWriter
from microprediction import new_key

def test_validate():
    write_key = new_key(difficulty=7)
    assert MicroWriter.is_valid_key(write_key)

def test_maybe():
    try:
        from microprediction.config_private import TRAFFIC_WRITE_KEY
    except:
        TRAFFIC_WRITE_KEY = new_key(difficulty=7)
    assert MicroWriter.is_valid_key(TRAFFIC_WRITE_KEY)

