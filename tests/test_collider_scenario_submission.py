from microprediction.collider import Collider
import numpy as np

mp = Collider(write_key='noise_trader_lkj897a9s8df7987sf_alkjfkljf')

def test_get_lagged_values():
    values = mp.get_lagged_values(name='cop.json')
    assert isinstance(values,list) and isinstance(values[0],float)

def test_get_current_value():
    values = mp.get_current_value(name='cop.json')
    assert isinstance(values, float)

def test_get_delayed_value():
    values = mp.get_delayed_value(name='cop.json')
    assert isinstance(values, float)


def test_predict():
    name = 'z1~cop.json'
    values = list( np.random.randn(1000) )
    res = mp.submit(name=name, values=values)
    assert res

def dont_test_get_balance():
    # Needs update to site
    bal = mp.get_balance()
