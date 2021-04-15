
from collections import OrderedDict
from microprediction.crawler import MicroCrawler
from microprediction.univariate.arrivals import approx_dt
from microconventions.stats_conventions import StatsConventions
import math
import numpy as np

from microconventions.stats_conventions import evenly_spaced_percentiles, nudged

# Video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started. There's a video explanation of FitCrawler, SequentialCrawler and friends
# at https://www.microprediction.com/fitcrawler


def split_k(approx_k:float):
    """ Represent a float 'k' as weighted combination of two integer ks  """
    l = math.floor(approx_k)
    u = math.ceil(approx_k)
    r = approx_k - l
    return (l, 1-r ), (u, r)


class StreamSkater(MicroCrawler):

    # Crawler utilizing the "skater" convention from the timemachines package,
    # and storing state on a stream basis (as compared with by horizon)

    ########################################################
    #  Override the following methods                      #
    ########################################################

    def __init__(self, f, n_warm:int=400, n_memory=450, use_std=False, **kwargs):
        """
            f         must be a "skater"
            n_warm    Number of historical data points to use the first time to warm up the skater
            n_memory  Number of recent points to use in generating the noise
            See https://github.com/microprediction/timemachines for explanation
        """
        super().__init__(**kwargs)
        self.f = f
        self.n_warm = n_warm
        self.n_memory = n_memory
        self.use_std = use_std
        self.stream_state = OrderedDict()

    def sample(self, lagged_values, lagged_times=None, name=None, delay=None, **ignored):
        """ Use skater to move and scale """

        if name not in self.stream_state:
            self.stream_state[name] = {'skater_state':{},
                                       'x':None,
                                       'x_std':None,
                                       'dt':None,
                                       't':None,
                                       'lookup':None} # Map from delay

        state = self.stream_state[name]

        if state['dt'] is None:
            # Initialize lookups from delay to steps ahead
            state['dt'] = approx_dt(lagged_times)
            state['lookup'] = dict([(dly, split_k( max(1,0.1+dly / (0.01 + state['dt']))-1)) for dly in self.DELAYS])
            state['k'] = int( math.ceil( (self.DELAYS[-1]+1.0)/state['dt'] ) )  # max k

        # Determine which observations are yet to be processed by the skater
        if state['t'] is None:
            ys = reversed( lagged_values[:self.n_warm] )
            ts = reversed( lagged_times[:self.n_warm] )
        else:
            all_t = reversed(lagged_times)
            all_y = reversed(lagged_values)
            yt = [ (y_,t_) for y_,t_ in zip(all_y,all_t) if t_>state['t']+1e-6 ]
            ys = [ yt_[0] for yt_ in yt ]
            ts = [ yt_[1] for yt_ in yt ]

        # Run the skater
        for y_,t_ in zip(ys,ts):
            state['x'], state['x_std'], state['skater_state'] = self.f(y=y_,s=state['skater_state'],k=state['k'],a=None,t=t_,e=None)
            state['t'] = t_

        # Interpolate point estimate and std errors
        (low_k,low_k_weight), (high_k, high_k_weight) = state['lookup'][delay]
        x_interp = low_k_weight*state['x'][low_k] + high_k_weight*state['x'][high_k]
        x_std_interp = low_k_weight*state['x_std'][low_k] + high_k_weight*state['x_std'][high_k]

        # Save stream state for next invocation
        self.stream_state[name] = state

        # Bootstrap default sample ... TODO move this elsewhere
        sc = StatsConventions()
        from tdigest import TDigest
        digest = TDigest()
        chronological_values = list(reversed(lagged_values))
        as_process = StatsConventions.is_process(chronological_values)
        xs = list(np.diff([0.] + chronological_values)) if as_process else chronological_values
        for x in xs:
            digest.update(x=x)
        default_samples = [digest.percentile(p * 100.) for p in StatsConventions.evenly_spaced_percentiles(num=self.num_predictions)]

        if not len(default_samples) == self.num_predictions:
            raise RuntimeError('Wrong number of samples in stream skater')

        # If not discrete, shift to match skater mean and standard deviation
        num_discrete_threshold = len(lagged_values)/2+5
        is_discrete = sc.is_discrete(lagged_values, num=num_discrete_threshold) or sc.is_discrete(np.diff(lagged_values),num=num_discrete_threshold)
        if is_discrete:
            # TODO: Find lattice and shift on lattice.
            return sc.nudged(default_samples)
        else:
            # Adjust mean of samples to match forecast
            shifted_samples = [ s + x_interp-np.mean(default_samples) for s in default_samples ]
            if not self.use_std:
                return sc.nudged(shifted_samples)
            else:
                samples_std = np.std(shifted_samples)
                if x_std_interp>0.5*samples_std and samples_std > 0.5*x_std_interp:
                    r = x_std_interp / samples_std
                else:
                    r = 1.0
                scaled_samples = [ s + r*(s-x_interp) for s in shifted_samples]
                return sc.nudged(scaled_samples)





