from microprediction.reader import MicroReader
from microconventions import api_url
import requests, pprint, time, json
from collections import OrderedDict

class MicroWriter(MicroReader):

    def __init__(self, write_key="invalid_key", base_url=None, verbose=True, **kwargs ):
        """ Create the ability to write """
        super().__init__(base_url=base_url or api_url(),**kwargs)
        string_write_key = write_key if isinstance(write_key,str) else write_key.decode()
        assert self.key_difficulty(string_write_key), "Invalid write_key. Mine one at muid.org. "
        self.write_key = string_write_key                 # Optional: location of your repo you wish to advertise
        self.verbose   = verbose
        self.code      = self.shash(write_key)            # Unique identifier that can be shared
        self.animal    = self.animal_from_key(write_key)  # ... and corresponding spirit animal

    def __repr__(self):
        return {'write_key':self.write_key,"animal":self.animal_from_key(self.write_key)}

    def get_own_repository(self):
        return self.get_repository(write_key=self.write_key)

    def set_repository(self, url):
        """ Tell everyone where your repository is """
        res = requests.put(self.base_url + '/repository/' + self.write_key, params={'url':url})
        if res.status_code == 200:
            return res.json()

    def delete_repository(self):
        """ Tell everyone where your repository is """
        res = requests.delete(self.base_url + '/repository/' + self.write_key)
        if res.status_code == 200:
            return res.json()

    def get_home(self):
        res = requests.put(self.base_url + '/live/' + self.write_key )
        if res.status_code == 200:
            return res.json()

    def set(self, name, value):
        """ Create or update a stream """
        res = requests.put(self.base_url + '/live/' + name, data={"write_key": self.write_key, "value": value})
        if res.status_code ==200:
            return res.json()
        elif res.status_code==500:
            raise Exception("server error")
        else:
            err = self.get_errors()[:2]
            pprint.pprint(err)
            print('',flush=True)
            raise Exception('Failed to update')

    def cset(self, names, values):
        """ Set multiple values linked by copula """
        request_data = {"names": ",".join(names), "write_key": self.write_key}
        request_data.update({"values": ",".join([str(v) for v in values])})
        res = requests.put(self.base_url + '/copula/', data=request_data)
        if self.verbose:
            pprint.pprint(res.content)
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 500:
            raise Exception("server error")
        else:
            err = self.get_errors()
            pprint.pprint(err)
            print('', flush=True)
            raise Exception('Failed to update')

    def touch(self, name):
        """ Extend TTL of stream without updating """
        res = requests.patch(self.base_url + '/live/' + name, data={"write_key": self.write_key})
        if res.status_code == 200:
            return res.json()
        else:
            err = self.get_errors()
            pprint.pprint(err)
            print('', flush=True)
            raise Exception('Failed to touch '+name)

    def get_errors(self):
        """ Retrieve private log information """
        res = requests.get(self.base_url + '/errors/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for '+ self.write_key)

    def delete_errors(self):
        """ Clear log of errors """
        res = requests.delete(self.base_url + '/errors/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def get_warnings(self):
        """ Retrieve private log information """
        res = requests.get(self.base_url + '/warnings/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def delete_warnings(self):
        """ Clear warnings """
        res = requests.delete(self.base_url + '/warnings/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def get_balance(self):
        res = requests.get(self.base_url + '/balance/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def put_balance(self, source_write_key, amount=100. ):
        """ Transfer some balance into self.write_key by reducing balance of source_write_key """
        res = requests.put(self.base_url + '/balance/' + self.write_key, data={"source_write_key": source_write_key,"amount":amount})
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def donate_balance(self, recipient_write_key, amount=100.):
        """ Give some of your balance to a key that has a negative balance """
        res = requests.put(self.base_url + '/balance/' + recipient_write_key,
                           data={"source_write_key": self.write_key, "amount": amount})
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def bolster_balance_by_mining(self,seconds=1):
        """ For a short time, try to burn a MUID to bolster flagging balance """
        key = self.maybe_create_key(difficulty=10,seconds=max(seconds,3))
        if key is not None:
            self.put_balance(source_write_key=key)
            return key

    def restore_balance_by_mining(self, difficulty=11):
        """ Mine a MUID and deposit it to bring the balance up from a negative number """
        source_write_key = self.create_key(difficulty=difficulty)
        return self.put_balance(source_write_key=source_write_key)

    def get_confirms(self):
        res = requests.get(self.base_url + '/confirms/' + self.write_key)
        if res.status_code == 200:
            confirm_strings = res.json()
            return [json.loads(c) for c in confirm_strings]
        else:
            raise Exception('Failed for ' + self.write_key)

    def get_infrequent_confirms(self):
        """ Everything except stream prediction and updates """
        COMMON = ['set','submit']
        return [c for c in self.get_confirms() if c.get('operation') not in COMMON]  # TODO: Move strings like 'withdraw' to microconventions

    def get_withdrawals(self):
        """ Get withdrawal confirmations """
        return [ c for c in self.get_confirms() if c.get('operation')=='withdraw'] # TODO: Move strings like 'withdraw' to microconventions

    def get_cancellations(self):
        """ Get cancellation confirmations, which can occur long after withdrawal requests """
        return [ c for c in self.get_confirms() if c.get('operation')=='cancel']

    def get_submissions(self):
        """ Get confirmations of submissions of predictions """
        return [c for c in self.get_confirms() if c.get('operation') == 'submit']

    def get_set_confirmations(self):
        """ Get confirmations of set operations """
        return [c for c in self.get_confirms() if c.get('operation') == 'set']

    def get_elapsed_since_confirm(self):
        confirms = self.get_confirms()
        if not confirms:
            return None
        last_confirm_time  = confirms[0].get("epoch_time")
        return time.time()-last_confirm_time

    def get_transactions(self, with_epoch=True):
        """
            :param with_timestamps bool     Set true to include epoch time (datetime already comes)
        """
        res = requests.get(self.base_url + '/transactions/' + self.write_key)
        if res.status_code == 200:
            transactions = res.json()
            transaction_values = [t[1] for t in transactions]
            if with_epoch:
                transaction_epoch_times = [ int(t[0].split('-')[0])/1000 for t in transactions ]
                for tv,tt in zip(transaction_values,transaction_epoch_times):
                    tv.update({'epoch_time':tt})
            return transaction_values
        else:
            raise Exception('Failed for ' + self.write_key)

    def get_elapsed_since_transaction(self):
        transactions = self.get_transactions(with_epoch=True)
        if not transactions:
            return None
        last_transaction_time  = transactions[0].get("epoch_time")
        return time.time()-last_transaction_time

    def get_active(self):
        res = requests.get(self.base_url + '/active/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def get_performance(self):
        res = requests.get(self.base_url + '/performance/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def delete_performance(self):
        res = requests.delete(self.base_url + '/performance/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def submit(self, name, values, delay=None, verbose=None):
        """ Submit prediction scenarios
        :param name:      str         Examples:    cop.json   z1~cop.json   z2~cop~qp.json
        :param write_key: str         Example:    "5263ee89-e34e-44dc-8b91-445b302b043e"
        :param values:    [ float ]
        :return: bool
        """
        verbose = verbose or self.verbose
        if delay is None:
            delay = self.DELAYS[0]
            print('It is suggested that you supply delay parameter to submit. Defaulting to shortest horizon but this will be removed in the future',flush=True)

        assert len(values)==self.num_predictions

        comma_sep_values = ",".join([ str(v) for v in values ] )
        res = requests.put(self.base_url + '/submit/' + name, data={'delay':delay, 'write_key': self.write_key, 'values': comma_sep_values})
        if res.status_code==200:
            if verbose:
                confirms = self.get_confirms()
                errors   = self.get_errors()
                pprint.pprint(confirms[-1:])
                pprint.pprint(errors[-1:])
                print('',flush=True)
            return True
        elif res.status_code==403:
            return False
        else:
            print('--- SUBMIT ERRORS ---- ')
            rrs = self.get_errors()[:2]
            pprint.pprint(rrs)
            print('',flush=True )
            raise Exception('Failed to submit')

    def cancel(self, name, delay=None, delays=None):
        """ Send request to cancel scenarios. However predictions won't be deleted immediately.

            :param  name    str
            :param  delay   int   or  delays [int]
            :returns bool

        """
        if delays is None and delay is None:
            delays = self.DELAYS
        elif delays is None:
            delays = [delay]
        codes = list()
        for delay in delays:
            res = requests.delete(self.base_url + '/submit/'+name, params={'write_key':self.write_key,'delay':delay} )
            codes.append(res.status_code)

        success   = all([ c==200 for c in codes ] )
        operating = all([ c in [200,403] for c in codes])
        if not operating:
            raise Exception('Failed to cancel.')
        else:
            return success

    def active_performance(self, reverse=False, performance=None, active=None):
        performance = performance or self.get_performance()
        active      = active or self.get_active()
        return OrderedDict(
            sorted([(horizon, balance) for horizon, balance in performance.items() if horizon in active],
                   key=lambda e: e[1], reverse=reverse))

    def worst_active_horizons(self, stop_loss, performance=None, active=None):
        """ Return horizons where we are losing more than stop_loss """
        return [horizon for horizon, balance in self.active_performance(reverse=True,performance=performance,active=active).items() if
                balance < -abs(stop_loss)]

    def cancel_worst_active(self, stop_loss, num=1000, performance=None, active=None):
        horizons = self.worst_active_horizons(stop_loss=stop_loss,performance=performance,active=active)[:num]
        for horizon in horizons:
            name, delay = self.split_horizon_name(horizon)
            self.cancel(name=name, delays=[delay])
            print('Cancelled participation in '+str(horizon),flush=True)
            time.sleep(0.1)
        return horizons