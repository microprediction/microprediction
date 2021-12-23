from microprediction import MicroReader
import random

# Live tests
mr = MicroReader(base_url='https://devapi.microprediction.org')
TEST_STREAM = random.choice(list(mr.get_streams().items()))[0]
DIE = 'die.json'
print(TEST_STREAM)


def test_getters():
    """ Not a great test :) """
    assert mr.get_current_value(DIE)
    assert len(mr.get_lagged_values(DIE)) > 10
    for delay in mr.DELAYS:
        p1 = mr.get_discrete_pdf_lagged(name=DIE, delay=delay )
        assert p1 is not None
        if p1.get('x'):
            assert abs(p1['y'][0] - 0.1666) < 0.15, "Oh man this die market is so inefficient!"


def test_z_getters():
    zs = mr.get_lagged_zvalues(name='z2~copula_x~copula_y~70.json', count=3)
    ps = mr.get_lagged_copulas(name='z2~copula_x~copula_y~70.json', count=3)
    assert len(zs)==3
    assert len(zs[0])==2
    assert len(ps) == 3
    assert len(ps[0]) == 2
    assert ps[0][0]<=1
    assert ps[0][0]>=0
    pass
