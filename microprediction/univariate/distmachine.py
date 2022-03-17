from copy import deepcopy
import numpy as np
from collections import OrderedDict


class DistMachine(object):

    # This is a state engine that has a ppf function
    # Example of usage: SequentialStreamCrawler
    # Subclasses: LossDist, FitDist

    def __init__(self, state, params: OrderedDict = None):
        self.params = params
        self.state = state

    def update(self, value=None, dt=None, **kwargs):
        # Incorporate new value, time passing, or both
        # Typically will update the state but not params
        raise NotImplementedError

    def inv_cdf(self, p: float) -> float:
        # Something like StatsConventions.norminv(p)
        raise NotImplementedError


class LossDist(DistMachine):

    # A distribution machine with a loss function

    def __init__(self, state: dict, params: OrderedDict = None):
        super().__init__(state=state, params=params)

    def log_likelihood(self, value: float) -> float:
        """ Likelihood for one value """
        raise NotImplementedError

    # Likelihood Distribution Machine comes with a default loss function, though you could
    # choose to augment or override this by adding other penalties (for instance adding penalty
    # for moving or back-tracking too much)

    def loss(self, lagged_values, lagged_times, params=None, state=None):
        """ Negative log-likelihood """

        def pre_getter(state, value, machine):
            return machine.log_likelihood(value=value)

        lls = self.replay(pre_getter=pre_getter, lagged_values=lagged_values, lagged_times=lagged_times,
                          params=params, state=state)
        return -np.sum(lls)

    def replay(self, lagged_values, pre_getter=None, post_getter=None, lagged_times=None, params=None, state=None):
        """ Run through data, return whatever getter retrieves from state

                state         set initial state
                params        set params
                pre_getter    get_iex_realtime_price( state, value, machine=None ) -> any   Before .update() called
                post_getter   get_iex_realtime_price( state, value, machine=None ) -> any   After  .update() called
                returns: [ pre_getter(), post_getter(), pre_getter(),... ] but omits if None
        """
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

        accumulated = list()
        for value, dt in zip(chronological_values, chronological_dt):
            if pre_getter is not None:
                accumulated.append(pre_getter(state=self.state, value=value, machine=self))
            self.update(dt=dt)
            if post_getter is not None:
                accumulated.append(post_getter(state=self.state, value=value, machine=self))
            self.update(value=value)
        self.params = saved_params
        self.state = saved_state
        return accumulated
