from microprediction.writer import MicroWriter
from microprediction.conventions import api_url
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


    def __init__(self, name, func, interval, write_key="invalid_key", base_url=None, verbose=True, func_args=None, mine= False, **kwargs):
        """  Create a stream by polling every 20 minutes, say
            param: name  str   stream name ending in .json
            func:        function    returns float  (data feed function)
            interval:    int     minutes between polls
            func_args    dict    optional dict of arguments to be passed to func
            mine:        bool    Supply mine=True if you want to automatically mine MUIDs to help keep the stream alive
        """
        assert self.is_valid_name(name),'name not valid'
        super().__init__(base_url=base_url or api_url(),write_key=write_key,verbose=verbose)
        self.name = name
        self.interval = interval
        self.func = func
        self.func_args = func_args
        self.recent = list()
        self.mining_time = 0
        self.mining_success = 0
        self.test_value = self.call_func()  # Fail fast
        self.mine = mine
        print('Created poller. Example value '+str(self.test_value))

    def __repr__(self):
        self_data= {'func':str(self.func),'interval':self.interval,'mining_time':self.mining_time}
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
        """ Mine just a little to avoid stream dying due to bankruptcy """
        if self.mine:
            balance = self.get_balance()
            if balance < 0:
                muid_time = time.time()
                key = self.bolster_balance_by_mining(seconds=max(5, int(abs(balance) / 10)))
                mining_time = time.time() - muid_time
                self.mining_time += mining_time
                if key:
                    print('************************')
                    print('     FOUND MUID !!!     ')
                    print('************************', flush=True)
                    self.mining_success += 1
                else:
                    print('Did not find MUID this time', flush=True)

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
            self.current_value = source_value
            if self.current_value is None:
                self.feed_state = ChangePoll.COLD
                self.alert(message='Something amiss with feed')
                return None
            else:
                self.current_value = float(source_value)
                value_change = float(self.current_value) - float(self.prev_value)
                if abs(value_change) < 1e-5:
                    self.feed_state = ChangePoll.COLD  # Feed is stale, don't judge
                    self.logger({'type':'feed_status','message':"****  Feed unchanged at " + str(datetime.datetime.now())})
                else:
                    self.prev_value = self.current_value
                    return value_change
        elif self.feed_state == ChangePoll.COLD:
            # Wait until feed is back up and speeds start changing
            self.prev_prev = self.prev_value if self.prev_value else None
            self.prev_value = source_value
            if (self.prev_value is not None) and (self.prev_prev is not None) and abs(
                    float(self.prev_prev) - float(self.prev_value)) > 1e-5:
                self.feed_state = ChangePoll.WARM
                self.logger({'type':'feed_status','message':'**** Feed resumed at ' + str(datetime.datetime.now())})
            return None




class MultiPoll(MicroPoll):

    # Create multiple streams updated at the same time

    # -------------------------------------------
    #  You may wish to override this method if the
    #  data retrieval function func() you provide
    #  does not return [ float ] or [ str ] that is
    #  convertable to float
    # --------------------------------------------

    def determine_next_values(self, source_values):
        """ Should receive raw source data and decides what to send, if anything

            :param source_values   [ float ] or whatever type is returned by self.func. Simplest would be [ float ]
            :returns  [ float ]  or None
        """

        if source_values is None or ( any( source_value is None for source_value in source_values) ):
            return None
        else:
            return [ float(sv) for sv in source_values ]

    # --------------------------------------------
    #  Maybe don't override the rest
    # --------------------------------------------

    def __init__(self, names, func, interval, write_key="invalid_key", base_url=None, verbose=True, func_args=None, with_copulas=False, **kwargs):
            """  Create a stream by polling every 20 minutes, say
                param: names  [ str ]    stream name ending in .json
                func:        function    returns raw data from some live source, ideally [ float ] but you can override determine_next_values method
                interval:    int         minutes between polls
                func_args    dict        optional dict of arguments to be passed to func

            """
            assert all( [ self.is_valid_name(name) for name in names]), 'name not valid'
            super().__init__(base_url=base_url or api_url(), write_key=write_key, verbose=verbose, func=func, func_args=func_args, interval=interval, name='never_used.json')
            self.names = names
            self.with_copulas = with_copulas

    def task(self):
        """ Scheduled task that runs every minute """
        start_time = time.time()
        data = {'start_time': str(datetime.datetime.now())}
        try:
            source_values = self.call_func()
        except Exception as e:
            source_values = None
        next_values = self.determine_next_values(source_values)
        data.update({'source_values': source_values,
                     'next_values': next_values,
                     'elapsed after polling': time.time() - start_time})
        # Send the data
        if next_values is None:
            res = {'operation':'touch','exec':[ self.touch(name=name) for name in self.names ]}
        elif self.with_copulas:
            res = self.cset(names=self.names, values=next_values )
        else:
            res = [ self.set(name=name,value=value) for name,value in zip(self.names, next_values) ]

        data.update({'values': next_values, "res": res, 'elapsed after sending': time.time() - start_time})
        self.logger(data=data)
        self.downtime()
        data.update({'elapsed after downtime': time.time() - start_time})



class MultiChangePoll(MultiPoll):

   COLD = 0
   WARM = 1

   def __init__(self, names, func, interval, write_key="invalid_key", base_url=None, verbose=True, func_args=None, with_copulas=False, **kwargs):
            """  Create multiple streams by polling every 20 minutes, say
                param:
                names        [ str ]    stream name ending in .json
                func:        function    returns data from some live source, ideally [ float ] but you can override determine_next_values method
                interval:    int         minutes between polls
                func_args    dict        optional dict of arguments to be passed to func
                with_copulas bool        Whether to create derived copula streams, or just individual unrelated streams
            """
            super().__init__(base_url=base_url or api_url(), write_key=write_key, verbose=verbose, func=func, func_args=func_args, interval=interval, names=names, with_copulas=with_copulas, **kwargs)
            self.prev_values = None
            self.feed_state = MultiChangePoll.COLD
            self.current_values = None

   def alert(self, message):
       print(message, flush=True)

   def determine_next_values(self, source_values):
       if self.feed_state == MultiChangePoll.WARM:
           # A warm state means that previous speed exists and is not stale
           assert self.prev_values is not None
           self.current_values = source_values
           if self.current_values is None:
               self.feed_state = MultiChangePoll.COLD
               self.alert(message='Something amiss with feed')
               return None
           else:
               self.current_values   = [ float(source_value) for source_value in source_values ]
               value_changes    = [ float(current_value) - float(prev_value) for current_value, prev_value in zip(self.current_values, self.prev_values) ]
               material_changes = [ abs(vc)>1e-6 for vc in value_changes ]
               if not any(material_changes):
                   self.feed_state = MultiChangePoll.COLD  # Feed is stale, don't judge
                   self.logger(
                       {'type': 'feed_status', 'message': "****  Feed unchanged at " + str(datetime.datetime.now())})
               else:
                   self.prev_values = self.current_values
                   return value_changes
       elif self.feed_state == MultiChangePoll.COLD:
           # Wait until feed is back up and values start changing
           self.prev_prev = self.prev_values if self.prev_values else None
           self.prev_values = source_values
           if (self.prev_values is not None) and (self.prev_prev is not None):
               material_changes = [abs(pp - pv) > 1e-6 for pp, pv in zip(self.prev_prev, self.prev_values)]
               if any( material_changes ):
                   self.feed_state = MultiChangePoll.WARM
                   self.logger({'type': 'feed_status', 'message': '**** Feed resumed at ' + str(datetime.datetime.now())})
           return None
       else:
           raise Exception('Brain failure')


