from microprediction.univariate.distmachine import LossDist
from abc import ABC
from collections import OrderedDict
from hyperopt import fmin, tpe, hp, STATUS_OK, STATUS_FAIL, Trials
from copy import deepcopy


# Distribution machine that can be fit (using hyperopt by default)


class FitDist(LossDist, ABC):

    def __init__(self, state: dict, params: OrderedDict, lower_bounds: dict = None, upper_bounds: dict = None,
                 space=None, algo=None, max_evals=10):
        """ Either supply hyperopt style 'space' object, or dictionaries with lower and upper bounds for every parameter """
        super().__init__(state=state, params=params)
        self.hyper_params = OrderedDict(
            {'lower_bounds': lower_bounds, 'upper_bounds': upper_bounds, 'space': space, 'algo': algo,
             'max_evals': max_evals})
        self.trials = Trials()

    def fit(self, lagged_values, lagged_times=None):
        params_before = deepcopy(self.params)  # Playing safe

        best_params, self.trials = self._hyperfit(lagged_values=lagged_values, lagged_times=lagged_times,
                                                  trials=self.trials, params=self.params,
                                                  **self.hyper_params)
        # Is it really better?
        loss_before = self.loss(lagged_values=lagged_values, lagged_times=lagged_times, params=params_before)
        loss_after = self.loss(lagged_values=lagged_values, lagged_times=lagged_times, params=best_params)
        changed = loss_after < loss_before
        if loss_after < loss_before:
            self.params.update(best_params)
        else:
            self.params = deepcopy(params_before)
        return changed

    # Implementation...

    def _hyperloss(self, prms, lagged_values, lagged_times=None):
        """ Same as loss but with hyperopt friendly signature

              prms:    list of values of parameters

        """
        params = OrderedDict(dict([(k, v) for k, v in zip(self.params.keys(), prms)]))
        evaluation = self.loss(lagged_values=lagged_values, lagged_times=lagged_times, params=params)
        try:
            evaluation = self.loss(lagged_values=lagged_values, lagged_times=lagged_times, params=params)
            status = STATUS_OK
        except Exception:
            evaluation = -99999999
            status = STATUS_FAIL

        return {'loss': evaluation, 'status': status}

    @classmethod
    def _hyperfit(lagged_values: [float], params: OrderedDict, lower_bounds: dict, upper_bounds: dict, lagged_times=None, space=None,
                  algo=None, max_evals=100, trials=None):

        if space is None:
            space = [hp.uniform(v, lower_bounds[v], upper_bounds[v]) for v in params]

        if algo is None:
            algo = tpe.suggest

        def fn(prms):
            return self._hyperloss(lagged_values=lagged_values, lagged_times=lagged_times, prms=prms)

        # Test a call to fn (easier stack trace)
        example_prms = list(params.values())
        test_value = fn(example_prms)

        # Re-evaluate trials on the more recent time series data
        new_evals = int(max_evals/2)

        trials = trials or Trials()
        if len(trials) > max_evals:
            trials = trials[-max_evals:]

        for trial in trials:
            vls = trial['misc']['vals']
            try:
                prms = [vls[k][0] for k in vls]  # FIXME: May not work for all spaces
                trial['result'] = fn(prms=prms)
            except IndexError:
                pass

        # Then try to find some new ones

        best_params = fmin(fn=fn, space=space, algo=algo, max_evals=new_evals, trials=trials)
        return best_params, trials
