# Provides an example of a self-navigating algorithm which you are under no obligation to use
from microprediction.writer import MicroWriter
from microprediction import new_key
from microconventions import api_url
import random, time, datetime
from microprediction.samplers import exponential_bootstrap, approx_mode
import pprint
import numpy as np
from statistics import median
import os


def new_key_if_none(write_key, use_environ=False, difficulty=10 ):
    """ Create key on the fly but warn user about time this may take

          :param   write_key str
          :param   use_environ bool     Highly experimental ... set True at your own risk
          :param   difficulty  int
          :returns write_key
    """
    if use_environ:
        write_key = write_key or os.environ.get('WRITE_KEY')
    if write_key is None:
        print('A write_key was not supplied, so burning one now of difficulty '+str(difficulty)+'. This will take a while, after which your crawler will be initialized. Save the write_key and next time supply a write_key to the constructor. ', flush=True)
        write_key = new_key(difficulty=difficulty)
        print('Your write_key is ' + write_key + '. Do not lose!! We recommend a quick visit to http://dev.microprediction.org/dashboard.html where you can punch it in')
        if use_environ:
            os.environ['WRITE_KEY'] = write_key
    return write_key


class MicroCrawler(MicroWriter):
    """To create a crawler you can derive from this class and it is suggested you overwrite one of more of the following methods:

           sample            - Method that creates predictions
           downtown          - Stuff to do when there is nothing terribly urgent

        You might also want to change

           candidate_streams  - A list of streams you want your crawler to look at. Alternatively override:
           include_stream
           exclude_stream
           candidate_delays   - A list of horizons to predict (from the set self.DELAYS). Alternativley override:
           include_delay
           exclude_delay
           update_frequency   - How many times to predict per arriving data point

       Good luck!
    """


    #############################################################
    #   Override these methods to select streamsa and horizons  #
    #############################################################


    def _default_candidate_streams(self):
        """ Suggests some streams based on arguments passed to constructor """
        budgets = self.get_budgets()
        sponsors = self.get_sponsors()
        # Stream criteria (combines with AND)
        not_too_dull = [name for name, budget in budgets.items() if float(budget) >= self.min_budget]
        not_too_competitive = [name for name, budget in budgets.items() if float(budget) <= self.max_budget]
        well_sponsored = [name for name, sponsor in sponsors.items() if self.include_sponsor(sponsor=sponsor)
                                                                and not self.exclude_sponsor(sponsor=sponsor)
                                                  and len(sponsor.replace(' ', '')) >= float(self.sponsor_min)]
        inclusion_criteria = [not_too_dull, not_too_competitive, well_sponsored]
        names = list(set.intersection(*map(set, inclusion_criteria)))
        return names

    def include_sponsor(self, sponsor=None, **ignore):
        """ Override this as you see fit to select streams for your crawler """
        return True

    def exclude_sponsor(self, sponsor=None, **ignore):
        """ Override this as you see fit to select streams for your crawler """
        return False

    def include_stream(self, name=None, **ignore):
        """ Override this as you see fit to select streams for your crawler
                   For example your crawler might like z streams or not, or might require
                   a minimum number of lags in the time series.
        """
        return True

    def exclude_stream(self, name=None, **ignore):
        """ Override this as you see fit to select streams for your crawler
                           For example your crawler might like z streams or not, or might require
                           a minimum number of lags in the time series.
        """
        return False

    def candidate_streams(self):
        """ Modify this as you see fit to select streams for your crawler
            For example your crawler might like z streams or not, or might require
            a minimum number of lags in the time series.

             :return [ str ]    List of stream names that your bot would be willing to participate in

        """
        names = self._default_candidate_streams()
        return [ n for n in names if self.include_stream(n) and not self.exclude_stream(n)]

    def include_delay(self, delay=None, name=None, **ignore):
        return True

    def exclude_delay(self, delay=None, name=None, **ignore):
        return False

    def candidate_delays(self, name=None):
        """  Determines how far ahead your bot is willing to predict.  However only valid delay times are acceptable (e.g 70)

            :returns [ int ]    List of horizons your bot is willing to participate in

            By all means override this if you want
        """
        return [d for d in self.DELAYS if self.include_delay(name=name, delay=d) and not self.exclude_delay(name=name, delay=d)]

    def update_frequency(self, name=None, delay=None):
        """ Determines how often to submit samples, measured in units of the typical time between data points
            Generally it is not necessary to update submissions quite as often for predictions that are changes
            of martingale-like quantities or for z-scores, z-curves.
        """
        return 20 if "~" in name else 1

    #################################################################
    #   Override these methods to change the statistical algorithm  #
    #################################################################

    def sample(self, lagged_values, lagged_times=None, name=None, delay=None, **ignored):
        """ An example of a sample method. This is where all the intelligence goes

               :param lagged_times [ float ]    List with most recent listed first
               :param lagged_times [ float ]    List of epoch times, most recent listed first
               :param name          str         Name of stream
               :param delay         int         Prediction horizon in seconds
               **ignored                        For future compatability.
               :returns            [ float ]    A vector of numbers somewhat indicative of a probability density, of length self.num_predictions

        """
        scenarios = exponential_bootstrap(lagged=lagged_values, num=self.num_predictions, decay=0.01)
        assert len(scenarios)==self.num_predictions, "Your sammpler should product a vector of length "+str(self.num_predictions)
        return sorted(scenarios)

    def downtime(self,seconds,**ignored):
        """ This will be called when a small gap opens up between times when you need to predict

               param: seconds  float    Number of seconds you have to spend doing whatever you please, since no prediction is due
               param: **ignored         For future compatability, allow passing of other parameters that, for now, you ignore.

            The function should return None.
        """
        time.sleep(seconds)

    #####################################################################
    #   Override these methods if you want additional things to happen  #
    #####################################################################

    def withdrawal_callback(self, horizon, **ignored):
        """ Override this if you want something additional to happen when your algorithm gives up on predicting a horizon
                  param: horizon   str


        """
        pass

    def startup_callback(self,**ignored):
        """ Override this if you want something additional to happen when your algorithm starts up

        """
        pass

    def retirement_callback(self, **ignored):
        """ Override this if you want something additional to happen when your algorithm totally gives up on life

        """
        pass

    def submission_callback(self, message, **ignored):
        """ Override this if you want something additional to happen when your algorithm make a submission
             param: message   dict
        """
        pass

    #############################################################################################
    #   Typically you don't want to override the rest of these, but its a free Python country   #
    #############################################################################################


    def __init__(self, write_key=None, base_url=None, verbose=False, quietude=50, stop_loss=10, min_budget=0., max_budget=10, min_lags = 25, max_lags=1000000, sponsor_min=12, use_environ=False, difficulty=10, max_active=20, **ignored):
        """
            param: write_key  str    Valid write_key    See www.microprediction.org or www.muid.com for more details
            param: base_url   str    e.g  'http://api.microprediction.org'  or 'http://devapi.microprediction.org' for the brave. Defaults to what is at http://config.microprediction.org
            param: verbose    bool   Verbosity parameter passed to MicroWriter
            param: quietude   int    If set to 10, will only barf messages 1/10th of the time
            param: stop_loss  float  How much to lose before giving up on a stream
            param: min_budget int
            param: max_budget int    These set the low/high limits for table stakes. See _default_candidate_streams() method
            param: min_lags   int
            param: max_lags   int    These set the short/long limits for the number of lags in a time series. Does your algo need or want a lot of data?
            param: sponsor_min int   Minimum write_key difficulty of the stream sponsor. E.g. set to 13 to only look at streams where people bothered to generate a 13-MUID.
            param: use_environ bool   Look in environ and store write_key
            param: difficulty  int   Used to create key if none supplied, but otherwise ignored
            param: **ignored        For future compatability

        """

        # Parameter management
        super().__init__(base_url=base_url or api_url(), write_key=new_key_if_none(write_key,use_environ=use_environ,difficulty=difficulty), verbose=verbose )
        assert self.key_difficulty(self.write_key) >= 7, "Invalid write_key for crawler. Use new_key(difficulty=11) to create one. "
        assert not self.base_url[-1]=='/','Base url should not have trailing /'
        assert stop_loss>0,"Stop loss must be positive "
        self.quietude    = int(quietude)       # e.g. if set to 10, will only print 1/10th of the time
        self.sponsor_min = sponsor_min         # Only choose streams with sponsors at least this long
        self.stop_loss   = stop_loss           # How much to lose before giving up on a stream
        self.min_budget  = min_budget          # Play with highly competitive algorithms?
        self.max_budget  = max_budget          # Play with highly competitive algorithms?
        self.min_lags    = min_lags            # Insist on historical data
        self.max_lags    = max_lags
        self.max_active  = max_active

        # Caching somewhat expensive operations to avoid taxing the system unnecessarily
        # There might be a tiny charge implemented for these operations at some point in the future
        self.performance = self.get_performance()
        self.active      = self.get_active()   # List of active horizons
        self.stream_candidates = self.candidate_streams()

        # State - times since ...
        self.seconds_until_next = 10
        self.last_performance_check = time.time()
        self.last_new_horizon = time.time()
        self.next_prediction_time = dict()  # Indexed by horizon
        self.last_withdrawal_reset = time.time()

        # State - other
        self.withdrawn  = list()           # List of horizons we have withdrawn from
        self.stopped = list()              # A list of horizons where we have hit stop loss and will not enter again
        self.next_prediction_time = dict() # A manifest of upcoming data arrivals
        self.message_log = list()          # A log of detailed messages

    def feel_like_talking(self):
        """ Override this, or set quietude parameter, to determine how often to barf longish messages """
        return self.quietude<=1 or random.choice(range(self.quietude))==0

    def upcoming(self,num=10, relative=True):
        """ List horizons and seconds until next prediction is required  """
        soon = sorted(self.next_prediction_time.items(), key=lambda d: d[1])[:num]
        if relative:
            t = time.time()
            return [ (n,int((s-t)*10)/10.0) for n,s in soon]
        else:
            return soon

    def update_seconds_until_next(self,exclude=None):
        exclude = exclude or list()
        upcoming = [t for h, t in self.upcoming(num=2, relative=True) if not h in exclude]
        try:
            self.seconds_until_next = min(upcoming)
        except:
            self.seconds_until_next = 10*60
        seconds_until_quit = self.end_time-time.time()
        if int(seconds_until_quit) in [1000,100,10,5]:
            print('Seconds until quit: '+str(seconds_until_quit),flush=True)
        self.seconds_until_next = min(self.seconds_until_next,seconds_until_quit)
        self.seconds_until_next = min(self.seconds_until_next, 5*60 )
        return self.seconds_until_next

    def __repr__(self):
        return {'quietude':self.quietude,
                'sponsor_min':self.sponsor_min,
                'stop_loss':self.stop_loss,
                'min_budget':self.min_budget,  # Get rid of this stuff
                'max_budget':self.max_budget,
                'min_lags':self.min_lags,
                'max_lags':self.max_lags,
                'num_active':len(self.active),
                'num_withdrawn':len(self.withdrawn),
                'current_balance':self.get_balance(),
                'recent_errors':self.get_errors()[-3:],
                'currently_worst': self.worst_active_horizons(stop_loss=self.stop_loss)[:10],
                'withdrawn': self.withdrawn,
                'upcoming':self.upcoming(num=3,relative=True)}

    def recent_updates(self):
        r = self.__repr__()
        return dict( [ (k,v) for k,v in r.items() if ('recent' in k or 'current' in k) ] )

    def withdraw(self,horizon):
        """
            Cancels participation in a horizon by withdrawing predictions, and adds to list of stopped out streams
        """
        name, delay = self.split_horizon_name(horizon)
        self.cancel(name=name, delays=[delay])
        horizon = self.horizon_name(name=name, delay=delay)
        if horizon in self.next_prediction_time:
            del self.next_prediction_time[horizon]
        self.withdrawn.append(horizon)
        self.stopped.append(horizon)
        print("Withdrawing from " + horizon, flush=True)
        self.active      = self.get_active()
        self.performance = self.get_performance()
        self.withdrawal_callback(horizon)

    def next_horizon(self, exclude=None):
        """
            Chooses a horizon that might be of interest to the algorithm
        """
        candidates = self.stream_candidates
        if exclude:
            candidates = [ c for c in candidates if not c in exclude ]
        if candidates:
            horizons = list()
            for name in candidates:
                delays = self.candidate_delays(name=name)
                for delay in delays:
                    horizon = self.horizon_name(name=name,delay=delay)
                    if not horizon in self.stopped:
                        if not horizon in self.active:
                            if not horizon in self.withdrawn:
                                if not (horizon in self.next_prediction_time) or time.time()>self.next_prediction_time[horizon]:
                                    horizons.append(horizon)
            if horizons:
                return random.choice(horizons)


    def expected_time_of_next_value(self, lagged_times):
        """
              Rudimentary estimate of the next time a data point will arrive based on history

              :returns  float, float      expected_at epoch time
                                          dt   typical time between data arrivals
        """
        if len(lagged_times) > 5:

            # Compute or assume time between data points
            neg_dt = approx_mode(np.diff(lagged_times))
            dt = -neg_dt if neg_dt is not None else None
            if dt is None:
                dt = self.DELAYS[-1]
            assert dt > 0
            if dt<10:
                dt = 10

            # Don't wait more than 6 hours
            if dt>(60*60*6):
                dt = 60*60*6

            # Compute expected time of next data point, but if data is missing move it forward
            # num_intervals>1 is used when we skip prediction, as with most z-curves for example
            expected_at = lagged_times[0] + dt
            if expected_at< time.time() + 45:
                expected_at = time.time() + dt
        else:
            expected_at = time.time() + self.DELAYS[-1]
            dt = self.DELAYS[-1]
        return expected_at, dt


    def set_next_prediction_time(self, lagged_times, delay, num_intervals):
        """
            Determine the next time at which we will make a prediction for a given horizon
        """
        # Called after making a prediction to determine when next to revisit the stream

        # First determine the time until the next data point, but if that is very soon we want the one after
        expected_at, dt = self.expected_time_of_next_value(lagged_times=lagged_times)

        while expected_at - time.time() < 20:
            expected_at = expected_at + dt

        # Anticipate predicting some time after arrival of the next data point
        # If num_intervals>1 we skip since updating is not considered necessary (e.g. z-curves)
        earliest = expected_at + 5  + (num_intervals-1)*dt
        latest   = expected_at + 10 + (num_intervals-1)*dt
        predict_time = np.random.rand()*(latest - earliest) + earliest
        assert predict_time>time.time()+40, 'prediction time too soon'

        return predict_time, dt, earliest, latest, expected_at

    def predict_and_submit(self, name, delay, lagged_times ):
        """
              Maybe submit a prediction
        """
        horizon = self.horizon_name(name=name, delay=delay)
        lagged_values = self.get_lagged_values(name)
        execut = 0
        message = {'name':name,'delay':delay,'submitted':False}
        if len(lagged_values) > self.max_lags:
            message.update({"reason": "Too many lags", "lagged_len": len(lagged_values)})
            self.withdraw(horizon)
            self.withdrawn.append(horizon)
        elif len(lagged_values or []) < self.min_lags:
            message.update({"reason": "Too few lags", "lagged_len": len(lagged_values)})
            if len(lagged_times)>5:
                dt = (lagged_times[1]-lagged_times[-1] )/(len(lagged_times)-1)
                next_predict_time = self.min_lags*dt + lagged_times[-1]
                if next_predict_time<time.time()+50:
                    next_predict_time = time.time()+50
                    print('Difficulty interpreting next prediction time for '+horizon+' as dt='+str(dt))
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
                            "min": scenario_values[0],
                            "max": scenario_values[-1]})

            num_intervals = self.update_frequency(name=name, delay=delay)
            predict_time, dt, earliest, latest, expected_at = self.set_next_prediction_time(lagged_times=lagged_times, delay=delay, num_intervals=num_intervals)
            message.update({'earliest': earliest, 'latest': latest})
            message.update({'expected_at':expected_at})
            self.next_prediction_time[horizon] = predict_time
            print('Submitted to ' + str(name) + ' ' + str(delay) +'s horizon, and will do so again in ' + str(int(self.next_prediction_time[horizon] - time.time())) + ' seconds.', flush=True)
            self.submission_callback(message=message)

            if not execut:
                message.update({"submitted":False,"reason":"execution failure","confirms":self.get_confirms()[-1:], "errors": self.get_errors()[-1:]})
                print("---------- Submission error ------------")
                pprint.pprint(message)
                print("-----------------------------")

        if self.feel_like_talking():
            message.update({'balance': self.get_balance(),
                            "errors":self.get_errors()[-10:]})
            print("Randomly sampled message: ")
            pprint.pprint(message)
            print(" ", flush=True)
        return execut

    def initial_next_prediction_time_multiplier(self, horizon):
        """
             Scales the initial time to make a prediction so that the algorithm doesn't get overwhelmed upon re-start.

        """
        return 5 if '~' in horizon else 1

    def status_report(self):
        """
            Barf some data about current status of horizons that are active or in the process of withdrawal
        """
        # By all means overwrite this for a less verbose crawler
        active_not_withdrawn = [a for a in self.active if not a in self.withdrawn]
        num_active = len(self.active)
        num_active_nw = len(active_not_withdrawn)
        print(self.animal + ' has active submissions for ' + str(num_active) + ' horizons ('+str(num_active_nw)+ ' with no withdrawal request pending since restart)',flush=True)
        withdrawal_confirms = self.get_withdrawals()
        cancellation_confirms = self.get_cancellations()
        num_recent_withdrawals    = len(withdrawal_confirms or [])
        num_recent_cancellations  = len(cancellation_confirms or [])
        if num_recent_cancellations or num_recent_withdrawals:
            print('Received recent confirmation of '+str(num_recent_withdrawals)+' requests to withdraw predictions and '+str(num_recent_cancellations)+' confirmed cancellations.',flush=True)
        print('Upcoming horizons and seconds to go ...',flush=True)
        pprint.pprint(self.upcoming(5))

    def withdraw_from_worst_active(self, stop_loss, num=1000, performance=None, active=None):
        horizons = self.worst_active_horizons(stop_loss=stop_loss,performance=performance,active=active)[:num]
        non_cancelled = [h for h in horizons if not h in self.withdrawn]
        for horizon in non_cancelled:
            self.withdraw(horizon=horizon)
            delay = int(float(self.split_horizon_name(horizon)[1]))
            effective_time = datetime.datetime.now() + datetime.timedelta(seconds=delay)
            print('Sent request to withdraw from participation in '+str(horizon)+' that will take effect in approximately '+str(delay)+' seconds, or around '+str(effective_time)+' GMT',flush=True)
            time.sleep(0.1)
        return horizons


    def run(self,timeout=None):
        """
            The crawler visits streams. It maintains a list of expected times at which new data points will arrive. At the annointed time(s), it
            submits predictions after the new data has arrived. It periodically looks for new horizons. It periodically withdraws from horizons where
            it is not faring too well (watch out for 'die' and 'coin_*' time series as they are simple but can lead to fast losses for some stock standard
            time series algorithms).

            This is just a suggestion. You can create very different crawlers using the MicroWriter class directly, should you wish to.

        """
        print(self.animal + " restarting at " + str(datetime.datetime.now()), flush=True)
        self.startup_callback()

        # Catch up on what we've missed
        self.performance = self.get_performance()
        self.active = self.get_active()
        self.start_time = time.time()
        self.end_time = time.time()+timeout if timeout is not None else time.time()+10000000
        self.last_performance_check = time.time()-1000
        self.last_new_horizon = time.time()-1000
        self.stream_candidates = self.candidate_streams()
        desired_streams = [self.horizon_name(stream_name, horizon) for stream_name in self.stream_candidates for horizon in [70, 310, 910]]
        self.next_prediction_time = dict( [ (stream, time.time() + k*self.initial_next_prediction_time_multiplier(stream)) \
            for k, stream in enumerate(self.active) if stream in desired_streams])
        pprint.pprint(self.__repr__())

        # Announce basics
        self.status_report()
        pprint.pprint(self.__repr__())

        catching_up = True
        while time.time()<self.end_time:

            # Reset withdrawal record just in case some occasionally fail ... defense
            overdue_for_withdrawal_reset = time.time()-self.last_withdrawal_reset>20*60
            if overdue_for_withdrawal_reset:
                self.withdrawn = []
                self.last_withdrawal_reset = time.time()
                print('Resetting withdrawal records', flush=True)

            # Withdraw if need be from losing propositions
            overdue_for_performance_check = (time.time()-self.last_performance_check > 5*60) or catching_up
            if overdue_for_performance_check:
                print('Checking performance ',flush=True)
                self.performance = self.get_performance()  # Expensive operation and may attract a small charge in the future
                self.active = self.get_active()
                self.withdraw_from_worst_active(stop_loss=self.stop_loss, performance=self.performance, active=self.active, num=50)
                self.last_performance_check = time.time()

            # Maybe we look for a new horizon to predict
            self.update_seconds_until_next()
            if len(self.active)<self.max_active:
                got_time_to_look = (self.seconds_until_next > random.choice( [1.0, 5.0, 20.0, 60.0, 120.0] )) or catching_up or len(self.active)<5
                been_a_while_since_last_horizon_added = (time.time()-self.last_new_horizon) > 60
                if got_time_to_look and (been_a_while_since_last_horizon_added or len(self.active)<5):
                    self.active = self.get_active()
                    self.stream_candidates = self.candidate_streams()
                    print('Currently predicting for ' + str(len(self.active)) + ' horizons but found '+ str(len(self.stream_candidates))+ ' candidate streams to examine.',flush=True)
                    horizon = self.next_horizon(exclude=self.withdrawn)
                    if horizon is None:
                        print('Cannot find another horizon. Crawler method next_horizon() did not suggest one. ',flush=True )
                    else:
                        name, delay = self.split_horizon_name(horizon)
                        lagged_times = self.get_lagged_times(name=name)
                        execut = self.predict_and_submit(name=name, delay=delay, lagged_times=lagged_times)  # Maybe will predict, maybe not
                        if not execut:
                            print('Declined horizon '+horizon,flush=True)
                        else:
                            print('Submitted to horizon '+horizon,flush=True)
                            self.last_new_horizon = time.time()

            # Then if there is still time, we might call the downtime() method
            self.update_seconds_until_next()
            if self.seconds_until_next>2 and not catching_up:
                downtime_seconds = min(30,self.seconds_until_next-1)
                print('Downtime for '+str(downtime_seconds)+'s',flush=True)
                self.status_report()
                self.downtime(seconds=downtime_seconds)
                self.update_seconds_until_next()

            if self.seconds_until_next<30:

                # If there isn't much time, just hang out and be ready
                if self.seconds_until_next>0:
                    time.sleep(self.seconds_until_next)

                # Make predictions in rapid succession until a gap opens
                go_time = time.time()
                num_upcoming_to_consider = 10 if not catching_up else 100
                for horizon, seconds_to_go in self.upcoming(num=num_upcoming_to_consider,relative=True):
                    seconds_since_game_time = time.time()-go_time
                    adjusted_seconds_to_go = seconds_to_go-seconds_since_game_time
                    if adjusted_seconds_to_go<2:
                        if adjusted_seconds_to_go>0:
                            time.sleep(adjusted_seconds_to_go)
                        name, delay  = self.split_horizon_name(horizon)
                        lagged_times = self.get_lagged_times(name=name)
                        data_arrived_recently = lagged_times and (abs(time.time()-lagged_times[0])<30)
                        if adjusted_seconds_to_go<-30 or data_arrived_recently:
                            name, delay = self.split_horizon_name(horizon)
                            self.predict_and_submit(name=name, delay=delay, lagged_times=lagged_times )
                        else:
                            self.next_prediction_time[horizon] = time.time()+delay

            else:
                # Conserve some CPU
                time.sleep(30)

            # Be nice and don't overwhelm system
            time.sleep(2.5)
            catching_up = False

        self.retirement_callback()
        self.status_report()
        print("Retiring gracefully at " + str(datetime.datetime.now()), flush=True)
        pprint.pprint(self.__repr__())
        pprint.pprint(self.recent_updates())









if __name__=="__main__":
    # Just an example write key... you'll need to get your own write_key  (see MUID.org or Micoprediction.org)
    from microprediction.config_private import FLASHY_COYOTE
    print(FLASHY_COYOTE,flush=True)

    # For the brave. Default API is https://api.microprediction.org
    base_url = 'https://devapi.microprediction.org'

    # Create crawler and run it
    crawler = MicroCrawler(base_url=base_url, write_key=FLASHY_COYOTE, stop_loss=3)
    crawler.run(timeout=50000)

