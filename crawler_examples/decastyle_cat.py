# An example of an online crawler

# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com
# New video tutorials are available at https://www.microprediction.com/python-1 to help you get started

from microprediction.onlinecrawler import OnlineStreamCrawler
from tdigest import TDigest
from microprediction.samplers import is_process, inv_cdf_walk
from microprediction.univariate.arrivals import approx_dt
import numpy as np
import math

try:
    from credentials import DECASTYLE_CAT as WRITE_KEY
except ImportError:
    raise EnvironmentError('You need a WRITE_KEY. See https://www.microprediction.com/private-keys')

# See statesboy_cat.py for a simpler way to achieve the same end

# An example of an online crawler

# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com
# New video tutorials are available at https://www.microprediction.com/python-1 to help you get started

from microprediction.onlinecrawler import OnlineStreamCrawler
from tdigest import TDigest
from microprediction.samplers import is_process, inv_cdf_walk
from microprediction.univariate.arrivals import approx_dt
import numpy as np
import math

try:
    from credentials import DECASTYLE_CAT as WRITE_KEY
except ImportError:
    raise EnvironmentError('You need a WRITE_KEY. See https://www.microprediction.com/private-keys')

# See statesboy_cat.py for a simpler way to achieve the same end


class DigestEquityCrawler(OnlineStreamCrawler):

    # This example maintains a running estimate of the CDF for each stream, using the tdigest library
    # TDigest maintains an efficient representation of CDF using k-means clustering
    # https://github.com/CamDavidsonPilon/tdigest
    #
    # t-Digest is so fast we don't really need separate updating in the downtown() method, so you may
    # choose not to derive from OnlineStreamCrawler. However this illustrates the pattern one can use
    # when periodic fitting would otherwise disrupt timely prediction.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def exclude_stream(self, name=None, **ignore):
        return '~' in name

    def include_stream(self, name=None, **ignore):
        return name[:2] == 'r_'

    def initial_state(self, name, **ignore):
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

    def sample(self, lagged_values, lagged_times=None, name=None, delay=None, **ignored):
        """ Sample absolute numbers, or differences added to last value """

        # You could modify this with any other anchor point gleaned from a point estimate
        # You could also take a larger number of walks and use tdigest to summarize into CDF

        if name not in self.queue:
            self.queue.update({name: self.initial_state(name=name)})

        state = self.queue[name]
        self.update_state(state=state, lagged_values=lagged_values, lagged_times=lagged_times)

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
    crawler = DigestEquityCrawler(write_key=WRITE_KEY)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/decastyle_cat.py')
    crawler.set_email("no_email@supplied.com")  # Only used to send you a voucher if you win a daily prize
    crawler.min_lags = 500
    crawler.run()

class DigestEquityCrawler(OnlineStreamCrawler):

    # This example maintains a running estimate of the CDF for each stream, using the tdigest library
    # TDigest maintains an efficient representation of CDF using k-means clustering
    # https://github.com/CamDavidsonPilon/tdigest
    #
    # t-Digest is so fast we don't really need separate updating in the downtown() method, so you may
    # choose not to derive from OnlineStreamCrawler. However this illustrates the pattern one can use
    # when periodic fitting would otherwise disrupt timely prediction.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def exclude_stream(self, name=None, **ignore):
        return '~' in name

    def include_stream(self, name=None, **ignore):
        return name[:2] == 'r_'

    def initial_state(self, name, **ignore):
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

    def sample(self, lagged_values, lagged_times=None, name=None, delay=None, **ignored):
        """ Sample absolute numbers, or differences added to last value """

        # You could modify this with any other anchor point gleaned from a point estimate
        # You could also take a larger number of walks and use tdigest to summarize into CDF

        if name not in self.queue:
            self.queue.update({name: self.initial_state(name=name)})

        state = self.queue[name]
        self.update_state(state=state, lagged_values=lagged_values, lagged_times=lagged_times)

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
    crawler = DigestEquityCrawler(write_key=WRITE_KEY)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/decastyle_cat.py')
    crawler.set_email("no_email@supplied.com")  # Only used to send you a voucher if you win a daily prize
    crawler.min_lags = 500
    crawler.run()
