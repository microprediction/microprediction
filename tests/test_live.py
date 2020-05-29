from microprediction.live import verrazano_speed, bronx_speed

def test_live():
    vs = float(verrazano_speed())
    bs = float(bronx_speed())

