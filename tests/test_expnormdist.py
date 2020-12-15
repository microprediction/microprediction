from microprediction.univariate.expnormdist import ExpNormDist, DEFAULT_EXPNORM_LOWER
import os
import numpy as np
from copy import deepcopy
import time
from microprediction import MicroReader

mr = MicroReader()
STREAMS = mr.get_stream_names()


DEFAULT_EXPNORM_PARAMS = {'g1': 0.5, 'g2': 5.0, 'logK': -2., 'loc': 0.0, 'logScale': 0.0}
DEFAULT_EXPNORM_LOWER = {'g1': 0.001, 'g2': 0.001, 'logK': -5, 'loc': -0.15, 'logScale': -4}
DEFAULT_EXPNORM_UPPER = {'g1': 1.0, 'g2': 15.0, 'logK': 1, 'loc': 0.15, 'logScale': 4.0}
OFFLINE_EXPNORM_HYPER = {'lower_bounds': deepcopy(DEFAULT_EXPNORM_LOWER),
                         'upper_bounds': deepcopy(DEFAULT_EXPNORM_UPPER),
                         'space': None, 'algo': None, 'max_evals': 3}


class ExpNormAccumulator(ExpNormDist):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def anchors(self, lagged_values, lagged_times):
        def post_getter(state,value):
            return state['anchor']
        return self.replay(lagged_values=lagged_values, lagged_times=lagged_times, post_getter=post_getter)

    def manual_loss(self, lagged_values, lagged_times, params, state, burn_in=10):
        """ Loss function for a series of values, calculated manually as check """
        # Lower the better
        assert len(lagged_values)>burn_in,'Too short to assign loss, no time to burn in'

        saved_params = deepcopy(self.params)
        saved_state = deepcopy(self.state)
        if params is None:
            params = self.params
        if state is None:
            state = self.state
        self.params = deepcopy(params)
        self.state = deepcopy(state)

        chronological_values = list(reversed(lagged_values))
        chronological_times = list(reversed(lagged_times))
        chronological_dt = [1.0] + list(np.diff(chronological_times))

        lls = list()
        for value, dt in zip(chronological_values, chronological_dt):
            self.update(dt=dt)
            lls.append( self.log_likelihood(value=value) )
            self.update(value=value)

        self.params = saved_params
        self.state = saved_state
        return -np.sum(lls)

def fake_lagged_values():
    return np.cumsum(np.random.randn(50))


def fake_lagged_times():
    return np.linspace(time.time(),time.time()+10000,50)


def test_fitting_and_loss():
    """ Pick a random stream and update parameters """
    lagged_values = fake_lagged_values()
    lagged_times = fake_lagged_times()
    machine = ExpNormAccumulator(hyper_params=OFFLINE_EXPNORM_HYPER)
    machine.fit(lagged_values=lagged_values, lagged_times=lagged_times)
    l1 = machine.manual_loss(lagged_values=lagged_values, lagged_times=lagged_times,
                             params=machine.params, state=machine.state)
    l2 = machine.manual_loss(lagged_values=lagged_values, lagged_times=lagged_times,
                             params=machine.params, state=machine.state)
    assert abs(l1-l2)<1e-4
