# Provides an example of a self-navigating algorithm which you are under no obligation to use

from microprediction.writer import MicroWriter
from microprediction.reader import default_url
import muid, random, time
from microprediction.samplers import exponential_bootstrap
import pprint
import numpy as np

class MicroCrawler(MicroWriter):

    def __init__(self, write_key=None, base_url=None, verbose=True, min_lagged=25, stop_loss=500, min_budget=0., max_budget=5., min_lags = 25, sponsor_min=12, sleep_time=300):
        """  """
        super().__init__(base_url=base_url or default_url(), write_key=write_key )
        assert muid.difficulty(write_key) >= 8, "Invalid write_key for crawler. See www.muid.org to mine one. "
        assert not self.base_url[-1]=='/','Base url should not have trailing /'
        self.verbose     = verbose
        self.min_lagged  = min_lagged          # Only consider streams with a long lag history
        self.sponsor_min = sponsor_min         # Only choose streams with sponsors at least this long
        self.sleep_time  = sleep_time          # Seconds to sleep between actions
        self.stop_loss   = stop_loss           # How much to lose before giving up on a stream
        self.min_budget  = min_budget          # Play with highly competitive algorithms?
        self.max_budget  = max_budget          # Play with highly competitive algorithms?
        self.min_lags    = min_lags            # Insist on historical data

    def choose_stream(self):
        """ Should return a stream name, or None """
        budgets     = self.get_budgets()
        sponsors    = self.get_sponsors()
        performance = self.get_performance()
        # Stream criteria (combines with AND)
        not_too_dull         = [name for name, budget in budgets.items() if float(budget) >= self.min_budget]
        not_too_competitive  = [name for name, budget in budgets.items() if float(budget) <= self.max_budget ]
        well_sponsored       = [name for name, sponsor in sponsors.items() if len(sponsor.replace(' ','')) >= float(self.sponsor_min)]
        inclusion_criteria   = [not_too_dull, not_too_competitive, well_sponsored]
        # Elimination criteria (AND NOT ...)
        unprofitable         = [name for name, balance in performance.items() if float(balance)<-self.stop_loss ]
        exclusion_criteria   = [ unprofitable ]
        # Choose at random
        inclusion = set.intersection(*map(set,inclusion_criteria))
        exclusion = set.intersection(*map(set,exclusion_criteria))
        candidates = [ c for c in inclusion if not c in exclusion ]
        if candidates:
            return random.choice(well_sponsored)

    def choose_horizon(self,name=None):
        return random.choice(self.delays)

    def create_prediction(self, lagged):
        """ Should return a vector of scenarios of len self.num_predictions """
        return exponential_bootstrap(lagged=lagged,num=self.num_predictions, decay=0.01)

    def predict_and_submit(self, name, delay):
        """ Given a stream and horizon, try to submit predictions """
        lagged = self.get_lagged_values(name)
        if len(lagged) < self.min_lagged:
            message = {'name': name, 'submitted': False, "reason": "Insufficient lags", "lagged_len": len(lagged)}
        else:
            scenario_values = self.create_prediction(lagged=lagged)
            exec = self.submit(name=name, values=scenario_values, delay=delay)
            balance = self.get_balance()
            message = {'name': name, "submitted": True, 'delay': delay, "values": scenario_values[:5],
                       "balance": balance,"exec":exec}
            if not exec:
                message.update({"submitted":False,"reason":"execution failure","confirms":self.get_confirms(), "errors": self.get_errors()})
        if self.verbose:
            pprint.pprint(message)
            print("", flush=True)
        return exec

    def withdraw(self,name):
        """ Stop participating in a stream """
        self.cancel(name=name)
        if self.verbose:
            print('Withdrawing from '+name,flush=True)

    def run(self):
        """ Run until it doesn't seem to be working anywhere """
        name = self.choose_stream()
        while name:

            # Withdraw from unprofitable streams
            performance = self.get_performance()
            for name, balance in performance.items():
                if float(balance)<-self.stop_loss:
                    self.withdraw(name=name)

            # Try to predict
            delay = self.choose_horizon(name=name)
            self.predict_and_submit(name=name, delay=delay)
            time.sleep(self.sleep_time)
            name = self.choose_stream()

        pprint.pprint(self.get_performance())
        print('Crawler is laying down to die ', flush=True )


    def initialization_checks(self):
        fake_lagged = list( np.random.randn(self.min_lagged) )
        scenarios    = self.create_prediction(fake_lagged)
        assert len(scenarios)==self.num_predictions, "This crawler will not work as the length of the "


