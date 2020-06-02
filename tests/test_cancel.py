from microprediction import new_key, MicroWriter
import numpy as np

def test_cancel_live():
    write_key = new_key(difficulty=7)
    predictor = MicroWriter(write_key=write_key, base_url='http://www.microprediction.com')
    values    = sorted(np.random.randn(predictor.num_predictions))
    predictor.submit(name='cop.json',values=values,delay=predictor.delays[0])
    res = predictor.cancel(name='cop.json')
    assert res, "Cancellation of submission failed"

