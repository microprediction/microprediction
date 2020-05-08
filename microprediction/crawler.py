# Provides an example of a self-navigating algorithm which you are under no obligation to use
from microprediction.writer import MicroWriter
from microprediction.reader import default_url
import muid, random, time
from collections import OrderedDict
from microprediction.samplers import exponential_bootstrap
import pprint
import numpy as np
import os
from statistics import mode, StatisticsError, median

def approx_mode(xs):
    xr = [ round(x) for x in xs]
    try:
        return mode(xr)
    except StatisticsError:
        return None


class MicroCrawler(MicroWriter):
    """Typically you will want to override one or more of the following methods:

           candidate_streams()                          Return a list of stream names
           candidate_horizons(name)                     Return int
           sample(lagged_values,lagged_times)           Creates samples from a vector of lagged value

       Good luck!
     """

    def __init__(self, write_key=None, base_url=None, verbose=False, quietude=50, stop_loss=100, min_budget=0., max_budget=100, min_lags = 25, max_lags=1000000, sponsor_min=12, sleep_time=300):
        """  """
        super().__init__(base_url=base_url or default_url(), write_key=write_key, verbose=verbose )
        assert muid.difficulty(write_key) >= 8, "Invalid write_key for crawler. See www.muid.org to mine one. "
        assert not self.base_url[-1]=='/','Base url should not have trailing /'
        assert stop_loss>0,"Stop loss must be positive "
        self.quietude    = int(quietude)       # e.g. if set to 10, will only print 1/10th of the time
        self.sponsor_min = sponsor_min         # Only choose streams with sponsors at least this long
        self.sleep_time  = sleep_time          # Minimum number of seconds to add between predictions on a given stream
        self.stop_loss   = stop_loss           # How much to lose before giving up on a stream
        self.min_budget  = min_budget          # Play with highly competitive algorithms?
        self.max_budget  = max_budget          # Play with highly competitive algorithms?
        self.min_lags    = min_lags            # Insist on historical data
        self.max_lags    = max_lags
        self.performance = self.get_performance()
        self.active      = self.get_active()
        self.horizon_blacklist = list()
        self.cancelled   = list()
        self.next_prediction_time = dict()
        self.backoff     = dict()              # Lookup of times to sleep when feeds are likely stale

    def feel_like_talking(self):
        return self.quietude<=1 or random.choice(range(self.quietude))==0

    def __repr__(self):
        return {'quietude':self.quietude,
                'sponsor_min':self.sponsor_min,
                'stop_loss':self.stop_loss,
                'min_budget':self.min_budget,
                'max_budget':self.max_budget,
                'min_lags':self.min_lags,
                'max_lags':self.max_lags,
                'num_active':len(self.active),
                'num_blacklisted':len(self.horizon_blacklist),
                'current_balance':self.get_balance(),
                'recently_erroneous':self.get_errors()[-3:],
                'currently_worst':self.worst_active_horizon()[:3],
                'recently_cancelled':self.cancelled[-3:],
                'recently_blacklisted': self.horizon_blacklist[-3:]}

    def recent_updates(self):
        r = self.__repr__()
        return dict( [ (k,v) for k,v in r.items() if ('recent' in k or 'current' in k) ] )

    def active_performance(self, reverse=False ):
        return OrderedDict( sorted( [ (horizon, balance) for horizon, balance in self.performance.items() if horizon in self.active], key = lambda e: e[1], reverse=reverse ) )

    def worst_active_horizon(self):
        return [ horizon for horizon, balance in self.active_performance(reverse=True).items() if balance<-abs(self.stop_loss) ]

    def cancel_worst_active(self,num=1):
        wap = self.worst_active_horizon()[:num]
        for horizon in wap:
            name, delay = self.split_horizon_name(horizon)
            self.cancel(name=name,delays=[delay])
            self.cancelled.append(horizon)
            print("Withdrawing from " + horizon, flush=True)
            self.horizon_blacklist.append(horizon)

    def candidate_streams(self):
        """ Should return a stream name list """
        budgets     = self.get_budgets()
        sponsors    = self.get_sponsors()
        # Stream criteria (combines with AND)
        not_too_dull         = [name for name, budget in budgets.items() if float(budget) >= self.min_budget]
        not_too_competitive  = [name for name, budget in budgets.items() if float(budget) <= self.max_budget ]
        well_sponsored       = [name for name, sponsor in sponsors.items() if len(sponsor.replace(' ','')) >= float(self.sponsor_min)]
        inclusion_criteria   = [not_too_dull, not_too_competitive, well_sponsored]

        candidates = list( set.intersection(*map(set,inclusion_criteria)))
        return candidates

    def candidate_delays(self, name=None):
        """ Should return a delay list """
        return self.delays

    def next_horizon(self, exclude=None):
        """ Choose an urgent horizon """
        candidates = self.candidate_streams()
        if exclude:
            candidates = [ c for c in candidates if not c in exclude ]
        if candidates:
            horizons = list()
            for name in candidates:
                delays = self.candidate_delays(name=name)
                for delay in delays:
                    horizon = self.horizon_name(name=name,delay=delay)
                    if not horizon in self.horizon_blacklist:
                        if not (horizon in self.next_prediction_time) or time.time()>self.next_prediction_time[horizon]:
                            horizons.append(horizon)
            if horizons:
                return random.choice(horizons)

    def cached_performance(self,name,delay):
        performance_key = os.path.splitext(name)[0] + self.sep() + str(delay)
        return self.performance.get(performance_key)

    def sample(self, lagged_values, lagged_times=None, name=None, delay=None):
        """ Should return a vector of scenarios of len self.num_predictions """
        return exponential_bootstrap(lagged=lagged_values,num=self.num_predictions, decay=0.01)

    def predict_and_submit(self, name, delay):
        """ Given a stream and horizon, try to submit predictions """
        lagged_values = self.get_lagged_values(name)
        lagged_times  = self.get_lagged_times(name)
        exec = 0
        if len(lagged_values or []) < self.min_lags or  len(lagged_values or []) > self.max_lags:
            message = {'name': name, 'submitted': False, "reason": "Insufficient or too many lags", "lagged_len": len(lagged_values)}
        else:
            scenario_values = self.sample(lagged_values=lagged_values,lagged_times=lagged_times, name=name, delay=delay )
            exec = self.submit(name=name, values=scenario_values, delay=delay)
            dt = -approx_mode(np.diff(lagged_times))
            if dt is None or self.sleep_time > dt:
                dt = self.sleep_time
            t_next = lagged_times[0] + dt
            horizon = self.horizon_name(name=name,delay=delay)
            if t_next>time.time():
                self.next_prediction_time[horizon] = t_next + 2
            else:
                print("Looks like " + name + " may be stale. Backing off. ")
                if horizon in self.backoff:
                    self.next_prediction_time[horizon] = time.time() + self.backoff[horizon]
                    self.backoff[horizon] = 2*self.backoff[horizon]
                else:
                    self.next_prediction_time[horizon] = time.time()+ delay
                    self.backoff[horizon] = delay

            balance = self.get_balance()
            message = {'name': name, "submitted": True, 'delay': delay, "median":median(scenario_values),"std":np.std(scenario_values), "values": scenario_values[:2], "balance": balance,"exec":exec}
            if not exec:
                message.update({"submitted":False,"reason":"execution failure","confirms":self.get_confirms()[-1:], "errors": self.get_errors()[-1:]})
        if self.feel_like_talking():
            pprint.pprint(message)
            print("", flush=True)
        return exec

    def initial_urgency_multiplier(self,horizon):
        """ Seconds """
        return 20 if '~' in horizon else 1

    def run(self):
        # Pick up where we left off, but stagger
        self.performance = self.get_performance()
        self.active = self.get_active()
        self.next_prediction_time = dict( [ (horizon, time.time() + k*self.initial_urgency_multiplier(horizon)) for k,horizon in enumerate(self.active)])
        pprint.pprint(self.__repr__())

        while True:

            # Period exploration and quitting
            if np.random.rand()<0.01 or len(self.next_prediction_time)==0:
                horizon = self.next_horizon(exclude=self.horizon_blacklist)
                name, delay = self.split_horizon_name(horizon)
                self.predict_and_submit(name=name, delay=delay)
                print(" ", )
                print(" Entering " + horizon)
                print(" ",flush=True )
                self.performance = self.get_performance()
                self.active = self.get_active()
                self.cancel_worst_active()
                if self.feel_like_talking():
                    print(" ")
                    pprint.pprint(self.recent_updates())
                    print(" ", flush=True)


            # Check if existing horizons need updated preictions
            for horizon, prediction_time in self.next_prediction_time.items():
                if time.time()>prediction_time:
                    name, delay = self.split_horizon_name(horizon)
                    self.predict_and_submit(name=name, delay=delay )

            # Chill out
            sleep_time = np.min( list(self.next_prediction_time.values() ) ) - time.time()
            if sleep_time>1:
                print('Sleeping for '+str(sleep_time))
                time.sleep(sleep_time)


    def initialization_checks(self):
        fake_lagged = list( np.random.randn(self.min_lags) )
        scenarios    = self.sample(fake_lagged)
        assert len(scenarios)==self.num_predictions, "This crawler will not work as the length of the "


