from microprediction.live.faang import portfolio_from_combination, scaled_portfolio_return
import numpy as np
import math


def test_return():
    no_changes = [0,0,0,0,0]
    wu = np.ones(5)/5.0
    w1 = [1.0,0,0,0,0]
    assert np.allclose( scaled_portfolio_return(changes=no_changes, w=wu ), 0 )

    for _ in range(4):
        ssr = 1000*math.log(1.1)+0.1*np.random.randn()  # scaled stock return
        changes = [ssr, 0, 0, 0, 0]
        spr = scaled_portfolio_return(changes=changes, w=w1)
        assert np.allclose( spr, ssr )



if __name__=='__main__':
    test_return()

