from microprediction.univariate.distmachine import LossDist
from abc import ABC
from collections import OrderedDict
from hyperopt import fmin, tpe, hp, STATUS_OK, STATUS_FAIL
from copy import deepcopy
from getjson import getjson
import json

# Distribution machine that can be fit (using hyperopt by default)

DEFAULT_HYPER_PARAMS = {'max_evals':15}


class FitDist(LossDist, ABC):

    def __init__(self, state: dict, params: OrderedDict, hyper_params:dict = None ):
        super().__init__(state=state, params=params)
        self.hyper_params = deepcopy(DEFAULT_HYPER_PARAMS)
        self.hyper_params.update(hyper_params)
        self.points_to_evaluate = list() # List of pretty good values from previous searches

    def fit(self, lagged_values, lagged_times=None):
        params_before = deepcopy(self.params)  # Playing safe
        state_before = deepcopy(self.state)

        best_params = self.hyperfit(lagged_values=lagged_values, lagged_times=lagged_times, **self.hyper_params)
        # Is it really better?
        if self.params is None:
            self.params.update(best_params)
            self.points_to_evaluate.append(best_params)
            changed = True
        else:
            loss_before = self.loss(lagged_values=lagged_values, lagged_times=lagged_times, params=params_before, state=state_before)
            loss_after  = self.loss(lagged_values=lagged_values, lagged_times=lagged_times, params=best_params, state=state_before)
            changed = loss_after < loss_before
            if loss_after < loss_before:
                self.params.update(deepcopy(best_params))
                self.points_to_evaluate.append(deepcopy(best_params))
            else:
                self.params = deepcopy(params_before)
        self.state = state_before
        return changed

    # Implementation...

    def _hyperloss(self, prms, lagged_values, lagged_times=None):
        """ Same as loss but with hyperopt friendly signature

              prms:    list of values of parameters

        """
        params = OrderedDict(dict([(k, v) for k, v in zip(self.params.keys(), prms)]))
        try:
            evaluation = self.loss(lagged_values=lagged_values, lagged_times=lagged_times,
                                   params=params, state=self.state)
            status = STATUS_OK
        except Exception:
            evaluation = -99999999
            status = STATUS_FAIL

        return {'loss': evaluation, 'status': status}

    def hyperfit(self, lagged_values: [float], lower_bounds: dict, upper_bounds: dict, lagged_times=None, space=None,
                 algo=None, max_evals=100 ):

        if space is None:
            if self.params is None:
                pass
            space = [hp.uniform(v, lower_bounds[v], upper_bounds[v]) for v in self.params]

        if algo is None:
            algo = tpe.suggest

        def fn(prms):
            return self._hyperloss(lagged_values=lagged_values, lagged_times=lagged_times, prms=prms)

        # Test a call to fn (easier stack trace)
        example_prms = list(self.params.values())
        test_value = fn(example_prms)

        max_points_to_evaluate = int(max_evals)/2
        if len(self.points_to_evaluate)>max_points_to_evaluate:
            self.points_to_evaluate = self.points_to_evaluate[-max_points_to_evaluate:]

        best_params = fmin(fn=fn, space=space, algo=algo, max_evals=max_evals,
                              points_to_evaluate=self.points_to_evaluate )
        return best_params





