# Examples of scenario generation models
import random, bisect
import numpy as np
import math
from scipy.stats import mode
from microprediction.univariate.cdfvalues import evenly_spaced_percentiles
from microprediction.univariate.processes import is_process
from microconventions.stats_conventions import StatsConventions
from microprediction.univariate.arrivals import approx_mode, approx_mode  # Imported for backward compatibility
from microprediction.univariate.processes import inv_cdf_walk  # Imported for backward compatibility
from scipy.interpolate import interp1d
from collections import Counter
from microprediction.univariate.arrivals import approx_dt


# Rudimentary utilities for generating samples for submission.


# --------------------------------------------------------------------------
#            Empirical discretization and basic utilities
# --------------------------------------------------------------------------

def implied_lattice(lagged_values):
    """ Collection of values which a time series is likely to take, assuming it is not continuous """
    q_lagged_values = np.round(lagged_values, decimals=5)
    q_lagged_lattice = sorted(list(set(q_lagged_values)))
    if 0.75 * len(q_lagged_values) > len(q_lagged_lattice) >= 2:
        dx = mode(np.diff(q_lagged_lattice)).mode[0]
        num_filled = int((q_lagged_lattice[-1] - q_lagged_lattice[0]) / dx) + 1
        filled_lattice = np.linspace(q_lagged_lattice[0], q_lagged_lattice[-1], num=num_filled)
        num_included = np.sum([x in filled_lattice for x in q_lagged_lattice])
        if num_included > 0.9 * len(q_lagged_lattice):
            return filled_lattice
        else:
            return q_lagged_values
    else:
        return q_lagged_values


def project_on_lagged_lattice(values, lagged_values):
    """ Ensure predictions lie on lattice implied by lagged_values
          values  samples that would be submitted were the data continuous
          returns: [ float ] samples that lie on lattice indicated by lagged_values
    """
    lattice = implied_lattice(lagged_values)
    nn_interpolator = interp1d(lattice, lattice, kind='nearest', bounds_error=False, fill_value='extrapolate')
    nearest = nn_interpolator(values)
    return nearest


def center_values_list(values, new_mean=None):
    if (new_mean is not None):
        prior_mean = np.nanmean(values)
        values = [v + new_mean - prior_mean for v in values]
    return values


def scale_values_list(values, new_std=None):
    if (new_std is not None) and (new_std > 0):
        prior_std = np.nanstd(values)
        prior_mean = np.nanmean(values)
        values = [(v - prior_mean) * (new_std / prior_std) + prior_mean for v in values]
    return values


def center_and_scale_values_list(values, new_mean=None, new_std=None):
    """
       Shift mean and/or adjust std
    """
    return scale_values_list(center_values_list(values=values, new_mean=new_mean), new_std=new_std)

# --------------------------------------------------------------------------
#          Recency bootstrappy things
# --------------------------------------------------------------------------


def exponential_bootstrap_projected(lagged_values, decay, num, as_process=None, new_mean=None, new_std=None):
    """ Returns bootstrampped samples taking values only on lattice implied by history """
    values = exponential_bootstrap(lagged=lagged_values, decay=decay, num=num, as_process=as_process)
    values = center_and_scale_values_list(values=values, new_mean=new_mean, new_std=new_std)
    return project_on_lagged_lattice(values=values, lagged_values=lagged_values)


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
    return StatsConventions.nudged(empirical_sample)


def differenced_bootstrap(lagged, decay, num):
    """ One parameter jiggled bootstrap favouring more recent observations (applied to differences processes) """
    safe_diff_lagged = np.diff(list(lagged) + [0., 0.])
    diff_samples = independent_bootstrap(lagged=safe_diff_lagged, decay=decay, num=num)
    return [lagged[0] + dx for dx in diff_samples]


# --------------------------------------------------------------------------
#            Gaussian
# --------------------------------------------------------------------------

def normal_sample(prediction_mean: float, prediction_std: float, num: int) -> [float]:
    """ Returns normally distributed samples evenly spaced in probability """
    return [prediction_mean + prediction_std * StatsConventions.norminv(p) for p in evenly_spaced_percentiles(num=num)]


def normal_sample_projected(prediction_mean: float, prediction_std: float, num: int, lagged_values):
    """ Returns normally distributed samples taking values only on lattice implied by history """
    values = normal_sample(prediction_mean=prediction_mean, prediction_std=prediction_std, num=num)
    return project_on_lagged_lattice(values=values, lagged_values=lagged_values)


# --------------------------------------------------------------------------
#           Gaussian implied by lagged values
# --------------------------------------------------------------------------

def gaussian_samples(lagged_values, num, as_process=None):
    as_process = as_process or is_process(lagged_values)
    return diff_gaussian_samples(lagged_values=lagged_values, num=num) if as_process else independent_gaussian_samples(
        lagged_values=lagged_values,
        num=num)


def independent_gaussian_samples(lagged_values, num):
    shrunk_std = np.nanstd(list(lagged_values) + [0.01, -0.01])
    shrunk_mean = np.nanmean(lagged_values + [0.0])
    return normal_sample_projected(prediction_mean=shrunk_mean, prediction_std=shrunk_std, num=num)


def diff_gaussian_samples(lagged_values, num):
    """ Samples from differences """
    safe_diff_lagged = np.diff(list(lagged_values) + [0., 0.])
    diff_samples = independent_gaussian_samples(lagged_values=safe_diff_lagged, num=num)
    return [lagged_values[0] + dx for dx in diff_samples]


# --------------------------------------------------------------------------
#            Ad-hoc
# --------------------------------------------------------------------------


def fox_sample(lagged_values, lagged_times, delay, num, name, as_process=None, new_mean=None, new_std=None):
    " Elementary but not completely woeful sampler, used by Malaxable Fox"
    dt = approx_dt(lagged_times)
    lag = max(10, math.ceil(delay / dt))
    print('lag = ' + str(lag))
    is_proc = as_process or ('~' not in name and StatsConventions.is_process(lagged_values))
    if len(lagged_values) < 250 + lag or not is_proc:
        values = exponential_bootstrap(lagged=lagged_values, decay=0.1, num=num, as_process=as_process)
        ret_values = StatsConventions.nudged(project_on_lagged_lattice(values=values, lagged_values=lagged_values))
    else:
        changes = np.diff(list(reversed(lagged_values)), n=lag)
        counter = dict(Counter(changes))
        d = dict(counter)
        num_total = len(changes)
        d1 = dict([(change, round(175 * change_count / num_total)) for change, change_count in d.items()])
        values = list()
        for change, rounded_count in d1.items():
            values.extend([change] * rounded_count)
        change_spray = list(range(-50, 50))
        values.extend(change_spray)
        change_values = values[:num]
        abs_values = [lagged_values[0] + chg for chg in change_values]
        if not len(abs_values) == num:
            # Too many rounded down ... may not be discrete
            abs_values = exponential_bootstrap(lagged=lagged_values, decay=0.1, num=num, as_process=True)
        ret_values = StatsConventions.nudged(project_on_lagged_lattice(values=abs_values, lagged_values=lagged_values))

    ret_values = center_and_scale_values_list(values=ret_values, new_mean=new_mean, new_std=new_std)

    return ret_values




# --------------------------------------------------------------------------
#            Helpers and backward compat
# --------------------------------------------------------------------------

def _weighted_random_sample(weights, num, population=None):
    try:
        return random.choices(weights=weights, k=num, population=population)
    except AttributeError:
        return _alternative_weighted_random_sample(weights=weights, k=num, population=population)


def _alternative_weighted_random_sample(weights, k, population=None):
    """ For way backward compatibility, can probably toss this """
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


if __name__ == '__main__':
    values = [-1, 0, 3, 3, 5, 5, 5, 5, 5, 6, 6, 6, 6, 9, 10, 11, 12]
    print(implied_lattice(values))
    values = [-1, 1, 1, -1, 1, 1]
    print(implied_lattice(values))
    values = np.random.randn(10)
    print(list(zip(values, project_on_lagged_lattice(values=values, lagged_values=[-2, -1, 0, 1, 2]))))
