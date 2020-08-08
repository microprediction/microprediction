from microprediction import MicroReader
import random

# Live tests
mr = MicroReader(base_url='https://devapi.microprediction.org')
TEST_STREAM = random.choice(list(mr.get_streams().items()))[0]
DIE = 'die.json'
print(TEST_STREAM)


def test_getters():
    assert mr.get_current_value(DIE)
    assert len(mr.get_lagged_values(DIE)) > 10
    for delay in mr.DELAYS:
        p1 = mr.get_discrete_pdf_lagged(name=DIE, delay=delay )
        assert p1 is not None
        assert abs(p1['y'][0] - 0.1666) < 0.1, "Oh man this die market is so inefficient!"
