# Illustrates use of t-digest, but without background fitting
# (A different way to skin the cat)

from microprediction.config_private import THALLODAL_CAT
from tdigest import TDigest
from microprediction.samplers import is_process, inv_cdf_walk, approx_dt
import numpy as np
import math
from microprediction.statefulcrawler import StreamCrawler


class DigestStreamCrawler(StreamCrawler):

    # Illustrates use of stateful StreamCrawler

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def exclude_stream(self, name=None, **ignore):
        return 'z3~' in name or 'z2~' in name

    def include_delay(self, delay=None, name=None, **ignore):
        return delay < 5000

    def initial_state(self, name, lagged_values, lagged_times, **ignore):
        """ Decide if it is a process or not, and create initial sketch of CDF of values or changes in values """
        # This is one off. Restarting may change the classification !
        values = self.get_lagged_values(name=name)
        times = self.get_lagged_times(name=name)
        digest = TDigest()
        as_process = is_process(values)
        data = np.diff(list(values) + [0., 0.]) if is_process(values) else values
        for value in data:
            digest.update(value)
        return {'t': times[0], 'digest': digest, 'as_process': as_process, 'dt': approx_dt(times), 'name': name}

    def update_state(self, state, lagged_values=None, lagged_times=None, **ignore):
        """ Use recently added values to update the digest """
        name = state['name']
        times = lagged_times or self.get_lagged_times(name=name)
        values = lagged_values or self.get_lagged_values(name=name)
        state['dt'] = approx_dt(times)
        new_values = [v for t, v in zip(times, values) if
                      t > state['t'] - 0.0001]  # Include one previous value in new_values, so we can difference
        new_data = np.diff(list(new_values)) if state['as_process'] else new_values[1:]
        for data in new_data:
            state['digest'].update(data)
        return state

    def sample_using_state(self, state, lagged_values, lagged_times, name, delay, **ignored):
        digest = state['digest']
        if state['as_process']:
            num_steps = int(math.ceil(delay / state['dt']))
            inv_cdf = lambda u: digest.percentile(u * 100)
            samples = sorted(
                [inv_cdf_walk(inv_cdf=inv_cdf, k=num_steps, x0=lagged_values[0]) for _ in range(self.num_predictions)])
        else:
            samples = [digest.percentile(p * 100.0) for p in self.percentiles()]
        return samples


if __name__ == "__main__":
    crawler = DigestStreamCrawler(write_key=THALLODAL_CAT, min_lags=500)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/thallodal_cat.py')
    crawler.min_lags = 500
    crawler.run()
