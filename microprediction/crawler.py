# Provides an example of a self-navigating algorithm which you are under no obligation to use
from microprediction.writer import MicroWriter
from microprediction.reader import default_url
import muid, random, time
from collections import OrderedDict
from microprediction.samplers import exponential_bootstrap, approx_mode
import pprint
import numpy as np
from statistics import median


class MicroCrawler(MicroWriter):
    """To create a crawler you can derive from this class (if you want) and it is suggested you overwrite one of more of the following methods:

           sample            - Method that creates predictions
           downtown          - Stuff to do when there is nothing terribly urgent

        You might also want to change

           candidate_streams  - A list of streams you want your crawler to look at
           candidate_delays   - A list of horizons to predict (from the set self.delays)
           update_frequency   - How many times to predict per arriving data point

       Good luck!
    """


    #############################################################
    #   Override these methods                                  #
    #############################################################


    def candidate_streams(self):
        """ Modify this as you see fit to select streams for your crawler
            For example your crawler might like z streams or not, or might require
            a minimum number of lags in the time series.

             :return [ str ]    List of stream names that your bot would be willing to participate in

        """
        budgets  = self.get_budgets()
        sponsors = self.get_sponsors()
        # Stream criteria (combines with AND)
        not_too_dull = [name for name, budget in budgets.items() if float(budget) >= self.min_budget]
        not_too_competitive = [name for name, budget in budgets.items() if float(budget) <= self.max_budget]
        well_sponsored = [name for name, sponsor in sponsors.items() if
                          len(sponsor.replace(' ', '')) >= float(self.sponsor_min)]
        inclusion_criteria = [not_too_dull, not_too_competitive, well_sponsored]
        names = list(set.intersection(*map(set, inclusion_criteria)))
        return names

    def candidate_delays(self, name=None):
        """  Determines how far ahead your bot is willing to predict.  However only valid delay times are acceptable (e.g 70)

            :returns [ int ]    List of horizons your bot is willing to participate in
        """
        return self.delays

    def update_frequency(self, name=None, delay=None):
        """ Determines how often to update samples """
        return 20 if "~" in name else 1 

    def sample(self, lagged_values, lagged_times=None, name=None, delay=None):
        """ An example of a sample method. This is where all the intelligence goes

               :param lagged_times [ float ]    Vector with most recent listed first
               :param lagged_times [ float ]    Vector of epoch times, most recent listed first
               :param name          str         Name of stream
               :param delay         int         Prediction horizon in seconds

         Swap this code out for whatever you choose to do.
         Return a vector of numbers somewhat indicative of a probability density, of length self.num_predictions

        """
        scenarios = exponential_bootstrap(lagged=lagged_values, num=self.num_predictions, decay=0.01)

        assert len(scenarios)==self.num_predictions, "Your sammpler should product a vector of length "+str(self.num_predictions)
        return sorted(scenarios)


    def downtime(self,seconds,**ignored):
        """ This will be called when a small gap opens up between times when you need to predict """
        # Be careful if you override it or you might be late for your next prediction
        time.sleep(seconds)

    #############################################################
    #   Typically don't want to override the rest of these      #
    #############################################################


    def __init__(self, write_key=None, base_url=None, verbose=False, quietude=50, stop_loss=10, min_budget=0., max_budget=10, min_lags = 25, max_lags=1000000, sponsor_min=12, sleep_time=300):
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
        self.message_log = list()
        self.seconds_until_next = 10           # Set just before self.sample() is called so we know how long we have
        self.last_performance_check = time.time()
        self.last_new_horizon = time.time()
        self.stream_candidates = self.candidate_streams()
        self.next_prediction_time = dict()     # Indexed by horizon

    def feel_like_talking(self):
        return self.quietude<=1 or random.choice(range(self.quietude))==0

    def upcoming(self,num=10, relative=True):
        """ List horizons and seconds until next prediction is required  """
        soon = sorted(self.next_prediction_time.items(), key=lambda d: d[1])[:num]
        if relative:
            t = time.time()
            return [ (n,s-t) for n,s in soon]
        else:
            return soon

    def update_seconds_until_next(self,exclude=None):
        exclude = exclude or list()
        upcoming = [t for h, t in self.upcoming(num=2, relative=True) if not h in exclude]
        try:
            self.seconds_until_next = min(upcoming)
        except:
            self.seconds_until_next = 10*60
        return self.seconds_until_next

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
                'currently_worst': self.worst_active_horizons()[:3],
                'recently_cancelled':self.cancelled[:3],
                'recently_blacklisted': self.horizon_blacklist[-3:],
                'backoff':sorted(self.backoff.items(),key=lambda d: d[1])[:3],
                'upcoming':self.upcoming(num=3,relative=True)}

    def recent_updates(self):
        r = self.__repr__()
        return dict( [ (k,v) for k,v in r.items() if ('recent' in k or 'current' in k) ] )

    def active_performance(self, reverse=False ):
        return OrderedDict( sorted( [ (horizon, balance) for horizon, balance in self.performance.items() if horizon in self.active], key = lambda e: e[1], reverse=reverse ) )

    def worst_active_horizons(self):
        return [ horizon for horizon, balance in self.active_performance(reverse=True).items() if balance<-abs(self.stop_loss) ]

    def withdraw(self,horizon):
        name, delay = self.split_horizon_name(horizon)
        self.cancel(name=name, delays=[delay])
        horizon = self.horizon_name(name=name, delay=delay)
        if horizon in self.next_prediction_time:
            del self.next_prediction_time[horizon]
        self.cancelled.append(horizon)
        print("Withdrawing from " + horizon, flush=True)
        self.horizon_blacklist.append(horizon)
        self.active      = self.get_active()
        self.performance = self.get_performance()

    def withdraw_from_worst(self, num=1):
        horizons = self.worst_active_horizons()[:num]
        for horizon in horizons:
            self.withdraw(horizon=horizon)

    def next_horizon(self, exclude=None):
        """ Choose an urgent horizon """
        candidates = self.stream_candidates
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

    def estimate_prediction_time(self, lagged_times, delay, num_intervals):
        # Base on lagged times of observations and the horizon, set a time at which to next create a prediction
        if len(lagged_times) > 5:
            neg_dt = approx_mode(np.diff(lagged_times))
            dt = -neg_dt if neg_dt is not None else None
            if dt is None or self.sleep_time > dt:
                dt = self.sleep_time
            # e.g. dt=90 and delay=310  we have 80 seconds grace
            expected_at = lagged_times[0] + dt * num_intervals
        else:
            expected_at = time.time() + 600
            dt = self.sleep_time

        if delay >= dt:
            earliest = expected_at + 5
            latest = expected_at + delay % dt - 5
        else:
            latest = expected_at - dt - 5
            earliest = expected_at - 2 * dt + 5
        if earliest > latest:
            earliest = latest
        predict_time = np.random.rand() * (latest - earliest) + earliest
        return predict_time, dt, earliest, latest, expected_at

    def predict_and_submit(self, name, delay, lagged_times ):
        """ Given a stream and horizon, try to submit predictions """
        horizon = self.horizon_name(name=name, delay=delay)
        lagged_values = self.get_lagged_values(name)
        execut = 0
        message = {'name':name,'delay':delay,'submitted':False}
        if len(lagged_values) > self.max_lags:
            message.update({"reason": "Too many lags - blacklisting", "lagged_len": len(lagged_values)})
            self.horizon_blacklist.append(horizon)
        if len(lagged_values or []) < self.min_lags:
            message.update({"reason": "Too few lags", "lagged_len": len(lagged_values)})
            if len(lagged_times)>5:
                dt = (lagged_times[1]-lagged_times[-1] )/(len(lagged_times)-1)
                next_predict_time = self.min_lags*dt + lagged_times[-1]
                if next_predict_time<time.time():
                    next_predict_time = time.time()+10*60*60
                    if not horizon in self.backoff:
                        self.backoff[horizon] = 10*60*60
            else:
                next_predict_time = time.time()+5*60
            self.next_prediction_time[horizon]=next_predict_time
            message.update({"next":next_predict_time,"in":next_predict_time-time.time()})
        else:
            # Call self.sample() but first let it know how much time it has
            self.update_seconds_until_next(exclude=[horizon])
            scenario_values = self.sample(lagged_values=lagged_values,lagged_times=lagged_times, name=name, delay=delay )
            execut = self.submit(name=name, values=scenario_values, delay=delay)
            message.update({'submitted':True,'exec':execut})
            message.update({"median": median(scenario_values),
                            "mean": np.mean(scenario_values),
                            "std": np.std(scenario_values),
                            "values[0]": scenario_values[0],
                            "values[-1]": scenario_values[-1]})

            num_intervals = self.update_frequency(name=name, delay=delay)
            predict_time, dt, earliest, latest, expected_at = self.estimate_prediction_time(lagged_times=lagged_times, delay=delay, num_intervals=num_intervals)
            message.update({'earliest': earliest, 'latest': latest})
            message.update({'expected_at':expected_at})

            if predict_time>time.time():
                message.update({'t_next':predict_time})
                self.next_prediction_time[horizon] = predict_time
            else:
                if horizon in self.backoff:
                    self.next_prediction_time[horizon] = time.time() + self.backoff[horizon]
                    self.backoff[horizon] = 2*self.backoff[horizon]
                else:
                    self.next_prediction_time[horizon] = time.time()+ delay
                    self.backoff[horizon] = delay
                message.update({'backoff':self.backoff[horizon]})

            if not execut:
                message.update({"submitted":False,"reason":"execution failure","confirms":self.get_confirms()[-1:], "errors": self.get_errors()[-1:]})
                print("---------- ERROR ------------")
                pprint.pprint(message)
                print("-----------------------------")

        if self.feel_like_talking():
            message.update({'balance': self.get_balance(),
                            "errors":self.get_errors()[-10:]})
            print(" ")
            pprint.pprint(message)
            print(" ", flush=True)
        return execut

    def initial_urgency_multiplier(self,horizon):
        """ Seconds """
        return 20 if '~' in horizon else 1

    def run(self):
        # Pick up where we left off, but stagger
        self.performance = self.get_performance()
        self.active = self.get_active()
        print('Currently predicting for ' + str(len(self.active)) + ' horizons')
        self.stream_candidates = self.candidate_streams()
        print('Found ' + str(len(self.stream_candidates)) + ' candidate streams.', flush=True)
        desired_streams = [self.horizon_name(stream_name, horizon) for stream_name in self.stream_candidates for horizon in [70, 310, 910]]
        self.next_prediction_time = dict( [ (stream, time.time() + k*self.initial_urgency_multiplier(stream)) \
            for k, stream in enumerate(self.active) if stream in desired_streams])


        print("---------- Restarting -------------")
        pprint.pprint(self.__repr__())
        print("-----------------------------------",flush=True)


        while True:

            # Periodically consider entering new horizons and withdrawing from others
            self.update_seconds_until_next()
            if self.seconds_until_next>np.random.randn()*120:
                if time.time()-self.last_performance_check>60*60:
                    self.performance = self.get_performance()
                    self.stream_candidates = self.candidate_streams()
                    print('Found '+str(len(self.stream_candidates))+ ' candidate streams.')
                    self.active = self.get_active()
                    print('Currently predicting for ' + str(len(self.active)) + ' horizons')
                    self.withdraw_from_worst()
                    self.last_performance_check = time.time()

            # If there is time consider entering a new stream, but not too often
            self.update_seconds_until_next()
            if (self.seconds_until_next>np.random.rand()*500) or (len(self.active)==0):
                if (time.time()-self.last_new_horizon>10*60) or (len(self.active)==0):
                    horizon = self.next_horizon(exclude=self.horizon_blacklist)
                    if horizon:
                        name, delay = self.split_horizon_name(horizon)
                        lagged_times = self.get_lagged_times(name=name)
                        self.predict_and_submit(name=name, delay=delay, lagged_times=lagged_times)
                        print(" ", )
                        print(" Found something new to predict: " + horizon)
                        print(" ",flush=True )
                        self.last_new_horizon = time.time()
                        if self.feel_like_talking():
                            print(" ")
                            pprint.pprint(self.recent_updates())
                            print(" ", flush=True)
                    else:
                        print(" ")
                        print(" Couldn't find anything else to predict, for now. ",flush=True )
                        print(" ",flush=True)

            # If there is time, maybe we chill, or do something productive like offline estimation
            self.update_seconds_until_next()
            if self.seconds_until_next>5:
                print('Downtime for '+str(self.seconds_until_next)+' seconds. Next '+ str(self.upcoming(num=1)))
                self.downtime(seconds=self.seconds_until_next-1)
                self.update_seconds_until_next()

            if self.seconds_until_next>0:
                time.sleep(self.seconds_until_next)

            # It might be time to submit predictions
            for horizon, seconds_to_go in self.upcoming(num=1,relative=True):
                name, delay = self.split_horizon_name(horizon)
                if seconds_to_go<1:
                    if seconds_to_go>0:
                        time.sleep(seconds_to_go+0.1)
                    lagged_times = self.get_lagged_times(name=name)
                    if lagged_times and (abs(time.time()-lagged_times[0])<30):
                        # Received recent data, so it is time to predict
                        name, delay = self.split_horizon_name(horizon)
                        self.predict_and_submit(name=name, delay=delay, lagged_times=lagged_times )
                    else:
                        time.sleep(1)




