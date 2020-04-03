# Provides an example of a self-navigating algorithm which you are under no obligation to use
from microprediction.writer import MicroWriter
from microprediction.reader import default_url
import muid, random, time
from collections import OrderedDict
from microprediction.samplers import exponential_bootstrap
import pprint
import numpy as np
import os

class MicroCrawler(MicroWriter):
    """Typically you will want to override one or more of the following methods:

           candidate_streams()                          Return a list of stream names
           choose_horizon(name)                         Return int
           sample(lagged_values,lagged_times)           Creates samples from a vector of lagged value

       Good luck!
     """

    def __init__(self, write_key=None, base_url=None, verbose=False, quietude=10, stop_loss=100, min_budget=0., max_budget=100, min_lags = 25, max_lags=1000000, sponsor_min=12, sleep_time=300):
        """  """
        super().__init__(base_url=base_url or default_url(), write_key=write_key, verbose=verbose )
        assert muid.difficulty(write_key) >= 8, "Invalid write_key for crawler. See www.muid.org to mine one. "
        assert not self.base_url[-1]=='/','Base url should not have trailing /'
        assert stop_loss>0,"Stop loss must be positive "
        self.quietude    = int(quietude)       # e.g. if set to 10, will only print 1/10th of the time
        self.sponsor_min = sponsor_min         # Only choose streams with sponsors at least this long
        self.sleep_time  = sleep_time          # Seconds to sleep between actions
        self.stop_loss   = stop_loss           # How much to lose before giving up on a stream
        self.min_budget  = min_budget          # Play with highly competitive algorithms?
        self.max_budget  = max_budget          # Play with highly competitive algorithms?
        self.min_lags    = min_lags            # Insist on historical data
        self.max_lags    = max_lags
        self.performance = self.get_performance()
        self.active      = self.get_active()
        self.stream_blacklist = list()
        self.cancelled   = list()

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
                'num_blacklisted':len(self.stream_blacklist),
                'current_balance':self.get_balance(),
                'recently_erroneous':self.get_errors()[-3:],
                'currently_worst':self.worst_active_horizon()[:3],
                'recently_cancelled':self.cancelled[-3:],
                'recently_blacklisted':self.stream_blacklist[-3:]}

    def recent_updates(self):
        r = self.__repr__()
        return dict( [ (k,v) for k,v in r.items() if ('recent' in k or 'current' in k) ] )

    def active_performance(self, reverse=False ):
        return OrderedDict( sorted( [ (horizon, balance) for horizon, balance in self.performance.items() if horizon in self.active], key = lambda e: e[1], reverse=reverse ) )

    def worst_active_horizon(self):
        return [ horizon for horizon, balance in self.active_performance(reverse=True).items() if balance<self.stop_loss ]

    def cancel_worst_active(self,num=1):
        wap = self.worst_active_horizon()[:num]
        for horizon in wap:
            name, delay = self.split_horizon_name(horizon)
            self.cancel(name=name,delays=[delay])
            self.cancelled.append(horizon)
            print("Withdrawing from " + horizon, flush=True)

    def candidate_streams(self):
        """ Should return a stream name, or None """
        budgets     = self.get_budgets()
        sponsors    = self.get_sponsors()
        # Stream criteria (combines with AND)
        not_too_dull         = [name for name, budget in budgets.items() if float(budget) >= self.min_budget]
        not_too_competitive  = [name for name, budget in budgets.items() if float(budget) <= self.max_budget ]
        well_sponsored       = [name for name, sponsor in sponsors.items() if len(sponsor.replace(' ','')) >= float(self.sponsor_min)]
        inclusion_criteria   = [not_too_dull, not_too_competitive, well_sponsored]
        # Choose at random
        candidates = list( set.intersection(*map(set,inclusion_criteria)))
        return candidates

    def choose_stream(self,exclude):
        candidates = self.candidate_streams()
        if exclude:
            candidates = [ c for c in candidates if not c in exclude ]
        if candidates:
            return random.choice(candidates)

    def cached_performance(self,name,delay):
        performance_key = os.path.splitext(name)[0] + self.sep() + str(delay)
        return self.performance.get(performance_key)

    def choose_delay(self, name):
        # Pick stream and horizon in seconds
        delay_choices = list()
        for delay in self.delays:
            horizon = self.horizon_name(name=name,delay=delay)
            if not horizon in self.cancelled:
                delay_choices.append(delay)
        if delay_choices:
            return random.choice(delay_choices)

    def sample(self, lagged_values, lagged_times=None):
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
            scenario_values = self.sample(lagged_values=lagged_values,lagged_times=lagged_times)
            exec = self.submit(name=name, values=scenario_values, delay=delay)
            balance = self.get_balance()
            message = {'name': name, "submitted": True, 'delay': delay, "values": scenario_values[:2], "balance": balance,"exec":exec}
            if not exec:
                message.update({"submitted":False,"reason":"execution failure","confirms":self.get_confirms()[-1:], "errors": self.get_errors()[-1:]})
        if self.feel_like_talking():
            pprint.pprint(message)
            print("", flush=True)
        return exec

    def run(self):

        # Pick up where we left off
        self.performance = self.get_performance()
        self.active = self.get_active()
        pprint.pprint(self.__repr__())
        name = self.choose_stream(exclude=self.stream_blacklist)

        # Randomly survey streams
        while name:
            # Get out of bad situations
            self.performance = self.get_performance()
            self.active = self.get_active()
            self.cancel_worst_active()
            if self.feel_like_talking():
                print(" ")
                pprint.pprint(self.recent_updates())
                print(" ",flush=True )

            # Consider entering a new one
            delay = self.choose_delay(name=name)
            if delay:
                self.predict_and_submit(name=name, delay=delay )
            else:
                self.stream_blacklist.append(name)

            # Next one ...
            time.sleep(self.sleep_time)
            name = self.choose_stream(exclude=self.stream_blacklist)

        print('Crawler is laying down to die ', flush=True )

    def initialization_checks(self):
        fake_lagged = list( np.random.randn(self.min_lags) )
        scenarios    = self.sample(fake_lagged)
        assert len(scenarios)==self.num_predictions, "This crawler will not work as the length of the "


