from microprediction.univariate.skewdist import SkewDist
from microconventions.stats_conventions import StatsConventions
import numpy as np


def test_skewdist():
    sd = SkewDist(num_predictions=250)
    xs = np.random.randn(100)
    for x in xs:
        sd.update(value=x)

    percentiles =  [0.25, 0.5, 0.75]
    skew_quantiles = [ sd.inv_cdf(p) for p in percentiles ]
    norm_quantiles = [ StatsConventions.norminv(p) for p in percentiles ]
    assert abs(skew_quantiles[1])<0.15
