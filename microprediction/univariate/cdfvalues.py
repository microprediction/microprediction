from microconventions.stats_conventions import is_discrete, evenly_spaced_percentiles, cdf_values, is_process, nudged, discrete_cdf, sign_changes, quantize
import numpy as np
from scipy.stats import mode
from scipy.interpolate import interp1d


def implied_lattice(lagged_values):
    """ Fill in gaps in discrete history """
    q_lagged_values = np.round(lagged_values,decimals=5)
    q_lagged_lattice = sorted(list(set(q_lagged_values)))
    if 0.75 * len(q_lagged_values) > len(q_lagged_lattice) >= 2:
        dx = mode(np.diff(q_lagged_lattice)).mode[0]
        num_filled = int((q_lagged_lattice[-1]-q_lagged_lattice[0])/dx)+1
        filled_lattice = np.linspace(q_lagged_lattice[0],q_lagged_lattice[-1],num=num_filled)
        num_included = np.sum([x in filled_lattice for x in q_lagged_lattice])
        if num_included>0.9*len(q_lagged_lattice):
            return filled_lattice
        else:
            return q_lagged_values
    else:
        return q_lagged_values


def project_on_lagged_lattice(values, lagged_values):
    """
          values  samples that would be submitted were the data continuous
          returns: [ float ] samples that lie on lattice indicated by lagged_values
    """
    lattice = implied_lattice(lagged_values)
    nn_interpolator = interp1d(lattice, lattice, kind='nearest', bounds_error=False, fill_value='extrapolate')
    nearest = nn_interpolator(values)
    return nearest


if __name__=='__main__':
    values = [-1,0,3,3,5,5,5,5,5,6,6,6,6,9,10,11,12]
    print(implied_lattice(values))
    values = [-1, 1, 1, -1, 1, 1]
    print(implied_lattice(values))
    values = np.random.randn(10)
    print(list(zip(values,project_on_lagged_lattice(values=values, lagged_values=[-2,-1,0,1,2]))))