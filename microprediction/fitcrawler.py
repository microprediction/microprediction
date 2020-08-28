from microprediction.univariate.fitdist import FitDist
from microprediction.sequentialcrawler import SequentialStreamCrawler
from typing import Type
from collections import OrderedDict
from queue import LifoQueue, Empty
from pprint import pprint
from microprediction.samplers import is_process
import math
import numpy as np
import random
import time

# Stream crawler that periodically fits parameters


class FitCrawler(SequentialStreamCrawler):

    def __init__(self, write_key, machine_type: Type[FitDist], state: dict = None, params: OrderedDict = None,
                 lower_bounds: dict = None, upper_bounds: dict = None, space=None, algo=None, max_evals=10,
                 min_seconds=20, min_elapsed = 5*60*60, decay=0.002, **kwargs):
        """
                state          -  Initial state of HyperDist objects
                params         -  Initial params of HyperDist objects
                lower_bounds, upper_bounds - An alternative to providing 'space'
                space          -  Hyperopt space object
                algo           -  Hyperopt algorithm choice
                max_evals      -  Number of hyperopt function evaluations to allow
                min_seconds    -  Minimum number of seconds we need in order to attempt fitting
                min_elapsed    -  Minimum time between attempts to fit a given time series

        """
        machine_params = {'state': state, 'params': params, 'lower_bounds': lower_bounds,
                          'upper_bounds': upper_bounds, 'space': space, 'algo': algo, 'max_evals': max_evals}
        super().__init__(write_key=write_key, machine_type=machine_type, machine_params=machine_params, **kwargs)
        self.fit_queue = list()          # List of streams that need fitting
        self.min_seconds = min_seconds   # Minimum time that must open up in order that we try to fit
        self.last_fit_time = dict()
        self.min_elapsed = min_elapsed
        self.decay = decay

    def fit(self, name, lagged_values, lagged_times=None, **ignored):
        """ Fit one stream, but only if the distribution machine supplied has a fit method """
        changed = False
        if name not in self.stream_state:
            self.stream_state.update(
                {name: self.initial_state(name=name, lagged_values=lagged_values, lagged_times=lagged_times)})
        else:
            machine = self.stream_state[name]['machine']
            changed = machine.fit(lagged_values=lagged_values, lagged_times=lagged_times)
            try:
                changed = machine.fit(lagged_values=lagged_values, lagged_times=lagged_times)
                if changed:
                    print('Found better params for ' + name)
                    pprint(machine.params)
                    print(' ', flush=True)
            except AttributeError:
                pass
        return changed

    def sample(self, lagged_values, lagged_times=None, name=None, delay=None, **ignored):
        """ Override default sampler so that we put the stream in the fit queue """

        if is_process(lagged_values):
            if name not in self.stream_state:
                self.stream_state.update(
                    {name: self.initial_state(name=name, lagged_values=lagged_values, lagged_times=lagged_times)})

            state = self.stream_state[name]
            state = self.update_state(state=state, lagged_values=lagged_values, lagged_times=lagged_times)
            samples = self.sample_using_state(state=state, lagged_values=lagged_values, lagged_times=lagged_times,
                                              name=name, delay=delay)
            self.stream_state[name] = state
            if name not in self.fit_queue:
                self.fit_queue.append(name)
            return samples
        else:
            # Flee cases where it isn't really a process
            for delay in self.DELAYS:
                horizon = self.horizon_name(name=name, delay=delay)
                self.withdraw(horizon=horizon)

    def downtime(self, seconds, **ignored):
        """ Try to fit then put on the end of the queue again """
        start_time = time.time()
        name = None
        if seconds > self.min_seconds:
            try:
                name = self.fit_queue.pop(0)
            except IndexError:
                pass
        if name is not None:
            if name not in self.last_fit_time or time.time()-self.last_fit_time[name]>self.min_elapsed:
                try:
                    lagged_values, lagged_times = self.get_lagged_values_and_times(name=name)
                except AttributeError:  # backward compat
                    lagged_values = self.get_lagged_values(name=name)
                    lagged_times = self.get_lagged_times(name=name)
                self.fit(name=name, lagged_values=lagged_values, lagged_times=lagged_times)
                self.fit_queue.append(name)
                self.last_fit_time[name] = time.time()
        seconds_used = time.time()-start_time
        seconds_remaining = seconds - seconds_used
        if seconds_remaining>1:
            super().downtime(seconds=seconds_remaining)

    def sample_using_state(self, state, lagged_values, lagged_times, name, delay, **ignored):
        """ Creates samples using previous walks """
        # Provides a default way to sample using state. Override as you see fit.

        chronological_values = list(reversed(lagged_values))
        chronological_times = list(reversed(lagged_times))
        chronological_dt = [1.0] + list(np.diff(chronological_times))
        dts = reversed(chronological_dt)
        num_steps = int(math.ceil(delay / state['dt']))

        from copy import deepcopy
        machine = deepcopy(state['machine'])

        # Walk back to get a good place to start
        for value,dt in zip(lagged_values,dts):
            machine.update(value=value)

        # Walk forward tracking anchor
        walk = list()
        for value, dt in zip(chronological_values, chronological_dt):
            machine.update(dt=dt)
            machine.update(value=value)
            anchor = machine.state['anchor']
            walk.append(anchor)

        # Sample randomly from walk and noise distribution, with some recently weighting for the former
        measurement_noise = [machine.inv_cdf(p) for p in self.percentiles()]
        steps_back = range(num_steps+1, len(lagged_values)-1)
        weights = [math.exp(-self.decay * lag) for lag in steps_back]
        back_choices = random.choices(population=steps_back, weights=weights, k=self.num_predictions)
        num = len(lagged_values)
        samples = [walk[num - step_back + num_steps] - walk[num - step_back] + noise for step_back, noise in
                   zip(back_choices, measurement_noise)]
        return sorted(samples)
