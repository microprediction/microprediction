from microprediction.univariate.skewdist import SkewDist
import numpy as np
from scipy.stats import skewnorm
import random


def test_skewdist():
    sd = SkewDist(num_interp=500)
    a = random.choice([2., 3., 4.])
    xs = skewnorm.rvs(a, size=1000)

    for x in xs:
        sd.update(value=x)

    percentiles = [0.25, 0.5, 0.75]
    skew_quantiles = [sd.inv_cdf(p) for p in percentiles]
    actual_quantiles = [np.quantile(xs, q) for q in percentiles]
    assert all(abs(z1 - z2) < 0.75 for z1, z2 in zip(skew_quantiles, actual_quantiles))

    sd_stats = [sd.state.mean, sd.state.var(), sd.state.skewness(), sd.state.kurtosis()]
    moment_comparison = list(zip(sd_stats, skewnorm.stats(a, moments='mvsk')))
    pass
