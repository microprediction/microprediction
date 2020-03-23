from microprediction.live import madison_bikes_available, verrazano_speed, bronx_speed

def test_live():
    ba = float(madison_bikes_available())
    vs = float(verrazano_speed())
    bs = float(bronx_speed())

