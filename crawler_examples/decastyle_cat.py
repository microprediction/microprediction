# An example of an online crawler


from microprediction.onlinecrawler import OnlineStreamCrawler
from tdigest import TDigest
from microprediction.samplers import is_process, approx_mode, inv_cdf_walk, approx_dt
import numpy as np
import math


class DigestCrawler(OnlineStreamCrawler):

    # This example maintains a running estimate of the CDF for each stream, using the tdigest library
    # TDigest maintains an efficient representation of CDF using k-means clustering
    # https://github.com/CamDavidsonPilon/tdigest

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def exclude_stream(self, name=None, **ignore):
        return 'z3~' in name or 'z2~' in name

    def initial_state(self, name, **ignore):
        """ Decide if it is a process or not, and create initial sketch of CDF of values or changes in values """
        # This is one off. Restarting may change the classification !
        values = self.get_lagged_values(name=name)
        times  = self.get_lagged_times(name=name)
        digest = TDigest()
        as_process = is_process(values)
        data = np.diff(list(values) + [0., 0.]) if is_process(values) else values
        for value in data:
            digest.update(value)
        return {'t':times[0],'digest':digest,'as_process':as_process,'dt':approx_dt(times),'name':name}

    def update_state(self, state, **ignore):
        """ Use recently added values to update the digest """
        name = state['name']
        times       = self.get_lagged_times(name=name)
        values      = self.get_lagged_values(name=name)
        state['dt'] = approx_dt(times)
        new_values = [ v for t,v in zip(times,values) if t>state['t']-0.0001 ] # Include one previous value in new_values, so we can difference
        new_data = np.diff(list(new_values)) if state['as_process'] else new_values[1:]
        for data in new_data:
            state['digest'].update(data)
        return state

    def sample(self, lagged_values, lagged_times=None, name=None, delay=None, **ignored):
        """ Sample absolute numbers, or differences added to last value """

        # You could modify this with any other anchor point gleaned from a point estimate
        # You could also take a larger number of walks and use tdigest to summarize into CDF

        if name not in self.queue:
            self.queue.update({name:self.initial_state(name=name)})

        state = self.queue[name]
        digest = state['digest']
        if state['as_process']:
            num_steps = int(math.ceil(delay/state['dt']))
            inv_cdf   = lambda u: digest.percentile(u*100)
            samples   = sorted([ inv_cdf_walk(inv_cdf=inv_cdf, k=num_steps, x0=lagged_values[0]) for _ in range(self.num_predictions)])
        else:
            samples   = [ digest.percentile(p*100.0) for p in self.percentiles() ]
        return samples


if __name__=="__main__":
    try:
        from microprediction.config_private import DECASTYLE_CAT
        crawler = DigestCrawler(write_key=DECASTYLE_CAT)
        crawler.set_repository(url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/decastyle_cat.py')
    except ImportError:
        crawler = DigestCrawler(difficulty=9)

    crawler.min_lags = 500
    crawler.run()