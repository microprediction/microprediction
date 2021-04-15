from collections import OrderedDict
from microprediction.crawler import MicroCrawler
from microprediction.univariate.arrivals import approx_dt
from microprediction.samplers import normal_sample_projected, project_on_lagged_lattice
from microprediction.univariate.processes import k_std
from microprediction.samplers import fox_sample
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

    # Crawler utilizing the timemachines package

    def __init__(self, f, n_warm:int=400, use_std=True, **kwargs):
        """
            f         must be a "skater"
            n_warm    Number of historical data points to use the first time to warm up the skater
            use_std   If True, we use the model standard deviation. If False, a simple estimate is preferred.
                      Be aware that some models from the timemachines package give dubious std error estimates.

        See https://github.com/microprediction/timemachines for explanation of "skaters", which are
        sequential online k-step ahead forecasting functions.
        """
        super().__init__(**kwargs)
        self.f = f
        self.n_warm = n_warm
        self.use_std = use_std
        self.stream_state = OrderedDict()


    #################################################
    #                                               #
    #   You'll likely want to override this ...     #
    #                                               #
    #################################################

    def sample_using_point_estimate(self, x:float, x_std:float, k, name, delay, lagged_values, lagged_times):
        """ Create 225 samples guided by a point estimate, and a standard deviation

              x      - point estimate returned by a function in the timemachines package (i.e. a "skater")
              x_std  - standard deviation of point estimate
              returns [float]

            By default this projects onto a lattice of values implied by the history
        """
        return normal_sample_projected(prediction_std=x, prediction_mean=x_std,
                                       num=self.num_predictions, lagged_values=lagged_values)


    #####################################################
    #                                                   #
    #   You'll likely not need to override this ...     #
    #                                                   #
    #####################################################

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

        # Create a hacky estimate of standard error, if necessary
        if not self.use_std:
            x_std_interp = k_std(lagged_values, k=high_k)

        return self.sample_using_point_estimate(x=x_interp, x_std=x_std_interp, k=high_k, name=name, delay=delay, lagged_values=lagged_values, lagged_times=lagged_times)


class SkatingFox(StreamSkater):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def sample_using_point_estimate(self, x:float, x_std:float, k:int, name:str, delay, lagged_values:[float], lagged_times):
        """ Create 225 samples guided by a point estimate, and a standard deviation
            Provided as an example of sub-classing StreamSkater, and modifying the sample generation.

                k  - Number of lags assumed to correspond to the delay

        """
        fox_samples = fox_sample(lagged_values=lagged_values, lagged_times=lagged_times, delay=delay,
                                 num=self.num_predictions, name=name)
        shifted_fox_samples = [ s + x - np.mean(fox_samples) for s in fox_samples ]
        r = x_std/np.std(fox_samples) if self.use_std else 1.0
        scaled_shifted_fox_samples = [ s + r*(s-x) for s in shifted_fox_samples ]
        return nudged(project_on_lagged_lattice(values=scaled_shifted_fox_samples, lagged_values=lagged_values))


class ChoosySkatingFox(SkatingFox):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def exclude_stream(self, name=None, **ignore):
        # Example of influencing the navigation
        return '~' in name or 'emoji' in name

    def include_delay(self, delay=None, name=None, **ignore):
        # Example of influencing choice of horizons to predict
        return delay < 10*60