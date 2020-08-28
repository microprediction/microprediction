from scipy.stats import exponnorm
from microprediction.univariate.fitdist import FitDist
from abc import ABC
from collections import OrderedDict
import math
import numpy as np
from microprediction.univariate.cdfvalues import evenly_spaced_percentiles
from copy import deepcopy
from microprediction.univariate.runningmoments import RunningVariance

# Example of a distribution that can be fitted using hyperopt


class ExpNormDist(FitDist, ABC):

    # This moves an anchor point using a two-parameter gain function
    # It judges likelihood based on a symmetric combination of expnorm distributions

    def __init__(self, params: OrderedDict = None, state=None):
        params = params or OrderedDict({'g1': 0.5, 'g2': 5.0, 'logK': -2.,'loc':0.0,'logScale':0.0})
        lower_bounds = {'g1': 0.001, 'g2': 0.001, 'logK': -5, 'loc': -0.15,'logScale':-4}
        upper_bounds = {'g1': 1.0, 'g2': 1.2, 'logK': 1, 'loc': 0.15,'logScale':4.0}
        state = state or {'anchor': None}
        super().__init__(params=params, state=state,
                         lower_bounds=lower_bounds, upper_bounds=upper_bounds)
        self.cached_params = None
        self.num_interp = 500
        self.cached_samples = None

    def update(self, value=None, dt=None, **kwargs):
        """ Move the anchor """
        if value is not None:
            dy = value - self.state['anchor'] if self.state['anchor'] is not None else 0.0
            move = self.params['g2'] * math.tanh(self.params['g1'] * dy / self.params['g2'])
            if self.state['anchor'] is not None:
                self.state['anchor'] = self.state['anchor'] + move
            else:
                self.state['anchor'] = value

    def log_likelihood(self, value: float) -> float:
        logK, loc, logScale = self.params['logK'], self.params['loc'], self.params['logScale']
        K = math.exp(logK)
        scale = math.exp(logScale)
        if self.state['anchor'] is None:
            return 0.0
        else:
            x = value - self.state['anchor']
            return math.log(
                exponnorm.pdf(x, K=K, loc=loc, scale=scale) + exponnorm.pdf(-x, K=K, loc=loc, scale=scale) + 0.001)

    def inv_cdf(self, p: float) -> float:
        """ PPF function for mixture of two exponorm distributions """
        if self.cached_samples is None or self.cached_params is None or self.params != self.cached_params or any(np.isnan(self.cached_samples)):
            logK, loc, logScale, num = self.params['logK'], self.params['loc'], self.params['logScale'], self.num_interp
            K = math.exp(logK)
            scale = math.exp(logScale)
            percentiles = evenly_spaced_percentiles(num=int(num / 2))
            cdf_1 = [exponnorm.ppf(p, K=K, loc=loc, scale=scale) for p in percentiles]
            cdf_2 = [-exponnorm.ppf(p, K=K, loc=loc, scale=scale) for p in percentiles]
            if len(cdf_1) + len(cdf_2) < num:
                cdf_1 = cdf_1 + [0]
            self.cached_samples = sorted(cdf_1 + cdf_2)
            self.cached_params = deepcopy(self.params)
        combined_percentiles = evenly_spaced_percentiles(self.num_interp)
        return np.interp(p, combined_percentiles, self.cached_samples)
