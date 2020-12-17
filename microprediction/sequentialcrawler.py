from microprediction.samplers import is_process, inv_cdf_walk
from microprediction.univariate.arrivals import approx_dt
import numpy as np
import math
from microprediction.statefulcrawler import StreamCrawler
from microprediction.univariate.distmachine import DistMachine
from microprediction.univariate.digestdist import DigestDist
from typing import Type
from copy import deepcopy

# Video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started. There's a video explanation of FitCrawler, SequentialCrawler and friends
# at https://www.microprediction.com/fitcrawler

class SequentialStreamCrawler(StreamCrawler):

    # Uses a DistributionMachine to make predictions (including processes with independent increments)

    ###################################################################################
    #   No need to change this class. Supply DistributionMachine type to constructor  #
    ###################################################################################

    def __init__(self, machine_type: Type[DistMachine] = DigestDist, machine_params=None, machine_state=None,  **kwargs):
        """
             **kwargs     : Arguments to MicroCrawler
             machine_type : Class
             machine_params : Listing of arguments that create default machine
        """
        super().__init__(**kwargs)
        self.machine_type   = machine_type
        self.machine_params = machine_params
        self.machine_state  = machine_state

    def initial_state(self, name, lagged_values, lagged_times, machine_params=None, machine_state=None, **ignore):
        # This is one off. Restarting may change the classification !
        chronological_values = list(reversed(lagged_values))
        chronological_times = list(reversed(lagged_times))
        as_process = is_process(chronological_values)
        values = list(np.diff([0.] + chronological_values)) if as_process else chronological_values
        dts = list(np.diff([chronological_times[0] - 1.0] + chronological_times))
        machine = self.machine_type(params=deepcopy( machine_params ), state=deepcopy( machine_state) )
        for value, dt in zip(values, dts):
            machine.update(value=value, dt=dt)
        return {'t': lagged_times[0], 'machine': machine, 'as_process': as_process, 'dt': approx_dt(lagged_times),
                'name': name}

    def update_state(self, state, lagged_values=None, lagged_times=None, **ignore):
        """ Use recently added values to update the machine """
        machine = state['machine']
        chronological_values = list(reversed(lagged_values))
        chronological_times = list(reversed(lagged_times))
        state['dt'] = approx_dt(chronological_times)
        new_data = [(t, v) for t, v in zip(chronological_times, chronological_values) if
                    t > state['t'] - 0.0001]  # Include one previous value in new_values, so we can difference
        new_chronological_values = list(np.diff([d[0] for d in new_data])) if state['as_process'] else [d[0] for d in
                                                                                                        new_data[1:]]
        new_chronological_dt = list(np.diff([d[0] for d in new_data]))
        for value, dt in zip(new_chronological_values, new_chronological_dt):
            machine.update(value=value, dt=dt)
        state['machine'] = machine
        return state

    def sample_using_state(self, state, lagged_values, lagged_times, name, delay, **ignored):
        """ Creates samples using Monte Carlo """
        machine = state['machine']
        if state['as_process']:
            num_steps = int(math.ceil(delay / state['dt']))
            samples = sorted(
                [inv_cdf_walk(inv_cdf=machine.inv_cdf, k=num_steps, x0=lagged_values[0]) for _ in
                 range(self.num_predictions)])
        else:
            samples = [machine.inv_cdf(p) for p in self.percentiles()]
        return samples

