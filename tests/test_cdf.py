from microprediction.reader import MicroReader

def test_get_cdf():
    cdf = MicroReader().get_cdf(name='cop.json')
