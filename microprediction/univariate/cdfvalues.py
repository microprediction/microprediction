from microconventions.stats_conventions import is_discrete, evenly_spaced_percentiles, cdf_values,\
    is_process, nudged, discrete_cdf, sign_changes, quantize, StatsConventions
import numpy as np

# Utilities to help with CDF's

from microprediction.univariate.arrivals import approx_mode

from microprediction.inclusion.scipyinclusion import using_scipy

if using_scipy:
    def robust_std(x):
        """ A robust measure of std """
        # Somewhat arbitrary!
        # https://en.wikipedia.org/wiki/Robust_measures_of_scale
        from scipy.stats import iqr, median_abs_deviation
        iqr_est = iqr(x)/1.349
        mad_est = 1.4826*median_abs_deviation(x)
        return np.nanmean([iqr_est,mad_est])

else:
    def robust_std(x):
        return np.nanstd(x)

