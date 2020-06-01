from microprediction.writer import MicroWriter
from microprediction.conventions import default_url
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from pprint import pprint
import datetime

class MicroPoll(MicroWriter):

    #--------------------------------------------
    #  You may wish to override these methods
    #--------------------------------------------

    def logger(self, data):
        """ Called after each attempt to poll data and send it """
        self.recent.append(data)
        if len(self.recent)>100:
            self.recent = self.recent[-100:]
        if self.verbose:
            pprint(data)
            print(' ',flush=True)

    def downtime(self):
        """ Also called after each attempt to send data """
        # By default it does a little MUID mining, or a little more if the balance is sinking
        self.maybe_bolster_balance_by_mining()


    def determine_next_value(self, source_value):
        """ Receives source data and decides what to send, if anything """
        # This should return a float or None
        return float(source_value) if source_value is not None else None

    #--------------------------------------------
    #  Probably don't want to override the rest
    #--------------------------------------------


    def __init__(self, name, func, interval, write_key="invalid_key", base_url=None, verbose=True, func_args=None, **kwargs):
        """  Create a stream by polling every 20 minutes, say
            param: name  str   stream name ending in .json
            func:        function    returns float  (data feed function)
            interval:    int     minutes between polls
            func_args    dict    optional dict of arguments to be passed to func
        """
        assert self.is_valid_name(name),'name not valid'
        super().__init__(base_url=base_url or default_url(),write_key=write_key,verbose=verbose)
        self.name = name
        self.interval = interval
        self.func = func
        self.func_args = func_args
        self.recent = list()
        self.mining_time = 0
        self.mining_success = 0
        self.test_value = self.call_func()  # Fail fast
        print('Created poller. Example value '+str(self.test_value))

    def __repr__(self):
        self_data= {'name':self.name,'func':str(self.func),'interval':self.interval,'mining_time':self.mining_time}
        if self.func_args is not None:
            self_data.update(self.func_args)
        return self_data

    def call_func(self):
        if isinstance(self.func_args,list):
            return self.func(*self.func_args)
        elif isinstance(self.func_args, dict):
            return self.func(**self.func_args)
        else:
            return self.func()

    def task(self):
        """ Scheduled task that runs every minute """
        start_time = time.time()
        data = {'start_time': str(datetime.datetime.now())}
        try:
            source_value = self.call_func()
        except Exception as e:
            source_value = None
        next_value   = self.determine_next_value(source_value)
        data.update({'source_value':source_value,
                     'next_value':next_value,
                     'elapsed after polling':time.time()-start_time})
        res = self.touch(self.name) if next_value is None else self.set(name=self.name, value=next_value)
        data.update({'value': next_value, "res": res,'elapsed after sending':time.time()-start_time})
        self.logger(data=data )
        self.downtime()
        data.update({'elapsed after downtime':time.time()-start_time})

    def maybe_bolster_balance_by_mining(self):
        """ Mine just a littel to avoid stream dying due to bankruptcy """
        balance = self.get_balance()
        if balance < 0:
            muid_time = time.time()
            key = self.bolster_balance_by_mining(seconds=max(50, int(abs(balance) / 10)))
            mining_time = time.time() - muid_time
            self.mining_time += mining_time
            if key:
                print('************************')
                print('     FOUND MUID !!!     ')
                print('************************', flush=True)
                self.mining_success += 1

    def run(self):
        data = {'type': 'scheduler', 'scheduler start time': time.time()}
        data.update(self.__repr__())
        self.logger(data=data)
        scheduler = BlockingScheduler()
        scheduler.add_job(self.task, 'interval', minutes=self.interval, max_instances=30)
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
        data.update({'stopping time':time.time()})
        self.logger(data=data)


class ChangePoll(MicroPoll):

    #    Illustrates predicting the change in a quantity ... when feed is not entirely reliable
    #    If we don't get good data from the feed or it appears to be stale, we don't publish the change

    COLD = 0
    WARM = 1

    def __init__(self, name, func, interval, write_key, func_args=None):
        super().__init__(name=name, func=func, interval=interval, func_args=func_args, write_key=write_key )
        self.prev_value = None
        self.feed_state = ChangePoll.COLD
        self.current_value = None

    def alert(self,message):
        print(message, flush=True)

    def determine_next_value(self, source_value):
        """ Returns a change if feed is warm, else None """

        if self.feed_state == ChangePoll.WARM:
            # A warm state means that previous speed exists and is not stale
            assert self.prev_value is not None
            current_value = source_value
            if current_value is None:
                self.feed_state = "cold"
                self.alert(message='Something amiss with feed')
                return None
            else:
                current_value = float(source_value)
                value_change = float(current_value) - float(self.prev_value)
                if abs(value_change) < 1e-5:
                    self.feed_state = "cold"  # Feed is stale, don't judge
                    self.logger({'type':'feed_status','message':"****  Feed unchanged at " + str(datetime.datetime.now())})
                else:
                    self.prev_value = current_value
                    return value_change
        elif self.feed_state == ChangePoll.COLD:
            # Wait until feed is back up and speeds start changing
            prev_prev = self.prev_value if self.prev_value else None
            prev_speed = source_value
            if (prev_speed is not None) and (prev_prev is not None) and abs(
                    float(prev_prev) - float(prev_speed)) > 1e-5:
                self.feed_state = ChangePoll.WARM
                self.logger({'type':'feed_status','message':'**** Feed resumed at ' + str(datetime.datetime.now())})
            return None


