import numpy as np
from microprediction.univariate.digestdist import DigestDist
from microprediction.univariate.distmachine import DistMachine
from microprediction.univariate.processes import is_process


# Utilities for constructing representative values that might be taken by a time series
# -------------------------------------------------------------------------------------

def is_discrete(lagged_values, num, ndigits=12):
    return len(set([round(x, ndigits) for x in lagged_values])) <= num


def evenly_spaced_percentiles(num):
    return list(np.linspace(start=1 / (2 * num), stop=1 - 1 / (2 * num), num=num))
    # [1. / (2 * num)] + list(1. / (2 * num) + np.cumsum((1 / num) * np.ones(num - 1)))


def cdf_values(lagged_values: [float], num, as_discrete=None):
    """ Default method of determining which abscissa are used for CDF's

        as_discrete   Supply bool if you know it

    """
    if as_discrete is None:
        as_discrete = is_discrete(lagged_values=lagged_values, num=num)

    if as_discrete:
        return cdf_discrete_values(lagged_values=lagged_values, num=num)
    else:
        return cdf_continuous_values(lagged_values=lagged_values, num=num)


def cdf_continuous_values(lagged_values: [float], num: int = 25, ndigits=2, machine: DistMachine = None) -> [float]:
    """ Returns a list of example values the time series might take next, based on recent lags

           num       Maximum number of sample values
           decimals  How to round values, which can be useful in reducing the number of calls
           machine   Supply an existing distribution machine to update it rather than starting afresh
           returns:  List of values of length not longer than num

    """
    # Uses t-digest
    chronological_values = list(reversed(lagged_values))
    as_process = is_process(chronological_values)
    xs = list(np.diff([0.] + chronological_values)) if as_process else chronological_values
    machine = machine or DigestDist()
    for x in xs:
        machine.update(value=x)
    sample_x = [machine.inv_cdf(p) for p in evenly_spaced_percentiles(num=num)]
    rounded_x = [round(x, ndigits) for x in sample_x]
    unique_x = list(set(rounded_x))
    return unique_x if not as_process else [chronological_values[-1] + x for x in unique_x]


def cdf_discrete_values(lagged_values: [float], num: int = 26, ndigits=6):
    chronological_values = list(reversed(lagged_values))
    as_process = is_process(chronological_values)
    xs = list(np.diff([0.] + chronological_values)) if as_process else chronological_values
    return quantize(xs, num=num, ndigits=ndigits)


def discrete_pdf(ys: [float]):
    """ Imply PDF from CDF in the discrete case only

           ys   Cumulative probabilities returned by get_cdf

    """
    # The get_cdf method is designed for continuous distributions.
    # In the case of discrete distributions it can be misleading.
    # We can recover the PDF in the special case where CDF x-values
    # are chosen to equal the finite set of values taken.
    # See https://gist.github.com/microprediction/ea63388c2bbcfd7623bd9937723565b9
    # for a worked example
    import math
    num = len(ys)
    mij = [[4 * math.pow(-1, i + k) for i in range(k)] + [2] + [0] * (num - k - 1) for k in range(num)]
    M = np.array(mij)
    pdf = np.matmul(M, ys)
    return list(pdf)


def discrete_cdf(cdf):
    """ Takes a raw CDF on discrete data and fixes it """
    pdf = discrete_pdf(cdf['y'])
    h = np.min(np.diff(cdf['x'])) / 10.0
    below = zip([x - h for x in cdf['x']], [0] + pdf[:-1])
    above = zip([x + h for x in cdf['x']], pdf)
    pairs = sorted(list(below) + list(above))
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    return {'x': xs, 'y': ys}


def quantize(xs, num: int, ndigits: int = 12):
    """ Round until there are less than or equal to num

            ndigits   Level of rounding to start at

    """
    if len(xs) <= num:
        return xs

    kdigits = ndigits
    while True:
        quantized_xs = set([round(x, kdigits) for x in xs])
        if len(quantized_xs) <= num:
            break
        kdigits = kdigits - 1

    return list(quantized_xs)
