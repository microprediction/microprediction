# Examples of scenario generation models
import random, bisect
import numpy as np
from microprediction.univariate.cdfvalues import evenly_spaced_percentiles
from microprediction.univariate.processes import is_process
from microconventions.stats_conventions import StatsConventions
from microprediction.univariate.arrivals import approx_mode, approx_mode  # for backward compatability
from microprediction.univariate.processes import inv_cdf_walk             # for backward compatability

# --------------------------------------------------------------------------
#          Recency bootstrappy things
# --------------------------------------------------------------------------
# Easy to understand but slightly lame default samplers.
# See also microprediction/univariate


def exponential_bootstrap(lagged, decay, num, as_process=None):
    as_process = as_process or is_process(lagged)
    return differenced_bootstrap(lagged=lagged, decay=decay, num=num) if as_process else independent_bootstrap(
        lagged=lagged, decay=decay, num=num)


def independent_bootstrap(lagged, decay, num):
    """ One parameter jiggled bootstrap favouring more recent observations
          lagged  [ float ]     List most recent observation first
          decay    float        Coefficient in exp(-a k) that weights samples
          num      int          Number of scenarios requested
           :returns  [ float ]  Statistical sample
    """
    weights = list(np.exp([-decay * k for k in range(len(lagged))]))
    empirical_sample = _weighted_random_sample(population=lagged, weights=weights, num=num)
    noise = np.random.randn(num)
    return [x + decay * eps for x, eps in zip(empirical_sample, noise)]


def differenced_bootstrap(lagged, decay, num):
    """ One parameter jiggled bootstrap favouring more recent observations (applied to differences processes) """
    safe_diff_lagged = np.diff(list(lagged) + [0., 0.])
    diff_samples = independent_bootstrap(lagged=safe_diff_lagged, decay=decay, num=num)
    return [lagged[0] + dx for dx in diff_samples]


# --------------------------------------------------------------------------
#            Gaussian
# --------------------------------------------------------------------------

def gaussian_samples(lagged, num, as_process=None):
    as_process = as_process or is_process(lagged)
    return diff_gaussian_samples(lagged=lagged, num=num) if as_process else independent_gaussian_samples(lagged=lagged,
                                                                                                         num=num)

def independent_gaussian_samples(lagged, num):
    shrunk_std = np.nanstd(list(lagged) + [0.01, -0.01])
    shrunk_mean = np.nanmean(lagged + [0.0])
    return [shrunk_mean + shrunk_std * StatsConventions.norminv(p) for p in evenly_spaced_percentiles(num)]


def diff_gaussian_samples(lagged, num):
    """ Samples from differences """
    safe_diff_lagged = np.diff(list(lagged) + [0., 0.])
    diff_samples = independent_gaussian_samples(lagged=safe_diff_lagged, num=num)
    return [lagged[0] + dx for dx in diff_samples]


# --------------------------------------------------------------------------
#            Helpers
# --------------------------------------------------------------------------

def _weighted_random_sample(weights, num, population=None):
    try:
        return random.choices(weights=weights, k=num, population=population)
    except AttributeError:
        return _alternative_weighted_random_sample(weights=weights, k=num, population=population)


def _alternative_weighted_random_sample(weights, k, population=None):
    """ way backward, can probably toss this """
    wrg = _WeightedRandomGenerator(weights)
    ndx = [wrg() for _ in range(k)]
    return ndx if population is None else [population[k] for k in ndx]


class _WeightedRandomGenerator(object):
    def __init__(self, weights):
        self.totals = []
        running_total = 0

        for w in weights:
            running_total += w
            self.totals.append(running_total)

    def next(self):
        rnd = random.random() * self.totals[-1]
        return bisect.bisect_right(self.totals, rnd)

    def __call__(self):
        return self.next()


