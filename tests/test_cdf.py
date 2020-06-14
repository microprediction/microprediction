from microprediction.reader import MicroReader

def test_get_cdf():
    mr = MicroReader()
    y,x = mr.get_cdf(name='cop.json')
