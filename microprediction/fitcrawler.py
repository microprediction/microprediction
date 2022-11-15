from microprediction.univariate.fitdist import FitDist
from microprediction.sequentialcrawler import SequentialStreamCrawler
from typing import Type
from collections import OrderedDict
from pprint import pprint
from microprediction.samplers import is_process
import math
import numpy as np
import random
import time
import logging
from copy import deepcopy
from microprediction.univariate.arrivals import approx_dt
from microprediction.univariate.cdfvalues import nudged
from getjson import getjson
from microprediction.samplers import project_on_lagged_lattice
from microconventions.stats_conventions import is_discrete

# Stream crawler that periodically fits parameters, or loads them
# Video explaining this code at https://www.microprediction.com/fitcrawler


class FitCrawler(SequentialStreamCrawler):

    def __init__(self, write_key, machine_type: Type[FitDist], machine_state: dict = None,
                 machine_params: OrderedDict = None,
                 lower_bounds: dict = None, upper_bounds: dict = None, space=None, algo=None, max_evals=10,
                 min_seconds=20, min_elapsed=5 * 60 * 60, decay=0.02, param_base_url=None, **kwargs):
        """
                state          -  Dictionary of state held for each stream. Supply None unless restarting.
                params         -  Initial params of HyperDist objects
                lower_bounds, upper_bounds - An easy alternative to providing hyperopt 'space'
                space          -  Hyperopt space object
                algo           -  Hyperopt algorithm choice (supply None to let it choose)
                max_evals      -  Total number of trials to keep (=hyperopt function evaluations per fitting)
                min_seconds    -  Minimum number of seconds that must open up before we attempt a fitting
                min_elapsed    -  Minimum time between attempts to fit a given time series

        """
        self.machine_hyper_params = {'lower_bounds': lower_bounds, 'upper_bounds': upper_bounds,
                                     'space': space, 'algo': algo, 'max_evals': max_evals}

        super().__init__(write_key=write_key, machine_type=machine_type, machine_params=machine_params,
                         machine_state=machine_state, **kwargs)
        self.fit_queue = list()  # List of streams that need fitting
        self.min_seconds = min_seconds  # Minimum time that must open up in order that we try to fit
        self.last_fit_time = dict()
        self.min_elapsed = min_elapsed
        self.decay = decay
        self.param_base_url = param_base_url   # Can be used to get offline parameters

    def include_delay(self, delay=None, name=None, **ignore):
        # It isn't recommended to use FitCrawler for long term predictions
        # Override if you are feeling bold
        return delay < 1000

    def initial_state(self, name, lagged_values, lagged_times, machine_params=None, machine_state=None, **ignore):
        #
        machine = self.machine_type(params=deepcopy(machine_params),
                                    state=deepcopy(machine_state),
                                    hyper_params=deepcopy(self.machine_hyper_params))

        chronological_values = list(reversed(lagged_values))
        chronological_times = list(reversed(lagged_times))
        as_process = is_process(chronological_values)
        values = list(np.diff([0.] + chronological_values)) if as_process else chronological_values
        dts = list(np.diff([chronological_times[0] - 1.0] + chronological_times))

        for value, dt in zip(values, dts):
            machine.update(value=value, dt=dt)
        return {'t': lagged_times[0], 'machine': machine, 'as_process': True, 'dt': approx_dt(lagged_times),
                'name': name}

    def fit(self, name, lagged_values, lagged_times=None, **ignored):
        """ Fit one stream, but only if the distribution machine supplied has a fit method """
        # Might use offline fit
        changed = False
        if name not in self.stream_state:
            self.stream_state.update(
                {name: self.initial_state(name=name, lagged_values=lagged_values, lagged_times=lagged_times)})
        else:
            machine = self.stream_state[name]['machine']

            stored_params = None
            if self.param_base_url is not None:
                url = self.param_base_url + '/' + name
                try:
                    stored_params = getjson(url)
                    if stored_params is None:
                        machine.params = stored_params
                except:
                    print('Failed to get params from '+url)

            if stored_params is None:
                try:
                    changed = machine.fit(lagged_values=lagged_values, lagged_times=lagged_times)
                    if changed:
                        print('Found better params for ' + name)
                        pprint(machine.params)
                        print(' ', flush=True)
                except (AttributeError, TypeError):
                    print('There was an error trying to use machine.fit inside fitcrawler')
                    print('Keeping the same params for ' + name)
                    pprint(machine.params)
                    print(' ', flush=True)

        return changed

    def sample(self, lagged_values, lagged_times=None, name=None, delay=None, **ignored):
        """ Override default sampler so that we put the stream in the fit queue """

        if is_process(lagged_values):
            if name not in self.stream_state:
                self.stream_state.update(
                    {name: self.initial_state(name=name, lagged_values=lagged_values, lagged_times=lagged_times,
                                              machine_state=self.machine_state, machine_params=self.machine_params)})
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
            if name not in self.last_fit_time or time.time() - self.last_fit_time[name] > self.min_elapsed:
                try:
                    lagged_values, lagged_times = self.get_lagged_values_and_times(name=name)
                except AttributeError:  # backward compat
                    lagged_values = self.get_lagged_values(name=name)
                    lagged_times = self.get_lagged_times(name=name)
                if lagged_values is None or lagged_times is None:
                    import logging
                    logging.warning("Could not fit " + name + " because we failed to get lagged_values ")
                else:
                    self.fit(name=name, lagged_values=lagged_values, lagged_times=lagged_times)
                    self.fit_queue.append(name)
                    self.last_fit_time[name] = time.time()

        seconds_used = time.time() - start_time
        seconds_remaining = seconds - seconds_used
        if seconds_remaining > 1:
            super().downtime(seconds=seconds_remaining)

    def sample_using_state(self, state, lagged_values, lagged_times, name, delay, **ignored):
        """ Creates samples using previous walks """
        # Provides a default way to sample using state. Override as you see fit.

        chronological_values = list(reversed(lagged_values))
        chronological_times = list(reversed(lagged_times))
        chronological_dt = [1.0] + list(np.diff(chronological_times))
        dts = reversed(chronological_dt)
        num_steps = int(math.ceil(delay / state['dt']))

        machine = deepcopy(state['machine'])

        # Walk back to get a good place to start
        for value, dt in zip(lagged_values, dts):
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
        steps_back = range(num_steps + 1, len(lagged_values) - 1)
        weights = [ math.exp(-self.decay * lag) for lag in steps_back ]
        back_choices = random.choices(population=steps_back, weights=weights, k=self.num_predictions)
        num = len(lagged_values)
        samples = [walk[num - step_back + num_steps] - walk[num - step_back] + noise for step_back, noise in
                   zip(back_choices, measurement_noise)]

        if is_discrete(lagged_values=lagged_values, num=0.75*len(lagged_values), ndigits=5):
            return project_on_lagged_lattice(values=samples, lagged_values=lagged_values)
        else:
            return sorted(nudged(samples))




