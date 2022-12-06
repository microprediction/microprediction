from microprediction.reader import MicroReader
from microconventions import api_url
from microconventions.value_conventions import ValueConventions
import requests, pprint, time, json
from collections import OrderedDict

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started creating streams and/or submitting predictions.


class MicroWriter(MicroReader):

    def __init__(self, write_key="invalid_key", base_url=None, verbose=True, **kwargs):
        """ Create the ability to write """
        super().__init__(base_url=base_url or api_url(), **kwargs)
        string_write_key = write_key if isinstance(write_key, str) else write_key.decode()
        assert self.key_difficulty(string_write_key), "Invalid write_key. Mine one at muid.org. "
        self.write_key = string_write_key  # Optional: location of your repo you wish to advertise
        self.verbose = verbose
        self.code = self.shash(write_key)  # Unique identifier that can be shared
        self.animal = self.animal_from_key(write_key)  # ... and corresponding spirit animal

    def __repr__(self):
        return json.dumps({'write_key': self.write_key, "animal": self.animal_from_key(self.write_key)})

    def get_own_repository(self):
        return self.get_repository(write_key=self.write_key)

    def get_own_predictions(self, name:str, delay:int, strip=True, consolidate=True ):
        """ Get predictions by others for a stream you own """
        return self.get_predictions(write_key=self.write_key,name=name, delay=delay, strip=strip, consolidate=consolidate)

    def set_repository(self, url):
        """ Tell everyone where your repository is """
        res = requests.put(self.base_url + '/repository/' + self.write_key, params={'url': url})
        if res.status_code == 200:
            return res.json()

    def set_email(self, email:str):
        """ Tell system, but not anyone else, your email """
        res = requests.put(self.base_url + '/email/' + self.write_key, params={'email': email})
        if res.status_code == 200:
            return res.json()

    def delete_repository(self):
        """ Tell everyone where your repository is """
        res = requests.delete(self.base_url + '/repository/' + self.write_key)
        if res.status_code == 200:
            return res.json()

    def get_home(self):
        res = requests.put(self.base_url + '/live/' + self.write_key)
        if res.status_code == 200:
            return res.json()

    def set(self, name, value, with_percentiles=False):
        """ Create or update a stream """
        if with_percentiles:
            data = {"write_key": self.write_key, "value": value, "with_percentiles":"1"}
        else:
            data = {"write_key": self.write_key, "value": value}
        res = requests.put(self.base_url + '/live/' + name, data)
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 500:
            raise Exception("server error")
        else:
            err = self.get_errors()[:2]
            pprint.pprint(err)
            print('', flush=True)
            raise Exception('Failed to update')

    def cset_in_chunks(self, names, values):
        """
           Call cset on moderate sized chunks to avoid straining system
        """
        CHUNK_SIZE = 250
        n = len(names)
        assert len(names)==len(values)
        chunks = [list(range(i, min(i + CHUNK_SIZE,n-1))) for i in range(0, n, CHUNK_SIZE)]
        if len(chunks)>1:
            chunks[-2] = chunks[-2]+chunks[-1] # Make sure there isn't a small chunk at the end
            chunks = chunks[:-1]
        last_res = None
        for chunk in chunks:
            try:
                names_chunk = [ names[j] for j in chunk]
                values_chunk = [ values[j] for j in chunk]
            except IndexError:
                print(chunk)
                raise NotImplementedError("WTF")
            last_res = self.cset(names=names_chunk, values=values_chunk)
        return last_res


    def cset(self, names, values):
        """ Set multiple values linked by copula """
        if len(names)>200:
            return self.cset_in_chunks(names=names, values=values)
        else:
            request_data = {"names": ",".join(names), "write_key": self.write_key}
            request_data.update({"values": ",".join([str(v) for v in values])})
            res = requests.put(self.base_url + '/copula/', data=request_data)
            print('Sent /copula/ request with '+str(len(names))+' names. ')
            if res.status_code == 200:
                res_json = res.json()
                if isinstance(res_json,list) and len(res_json)>20:
                    res_json = res_json[:5] + res_json[-5:]
                return res_json
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
            raise Exception('Failed to touch ' + name)

    def delete_state(self, k: int = 0):
        """ Delete remotely stored state """
        res = requests.delete(self.base_url + '/state/' + self.write_key, params={'k': k})
        if res.status_code == 200:
            return res.json()

    def get_state(self, k: int = 0):
        """ Get remotely stored state """
        res = requests.get(self.base_url + '/state/' + self.write_key, data={'k': k})
        if res.status_code == 200:
            return self.from_redis_value(res.json())

    def set_state(self, value, k: int = 0):
        """ Set remotely stored state

              value   dict, list, str
              k       int               Optional logical index from 0 to 319
              returns dict

            See https://github.com/microprediction/microstate for current memory size restrictions

        """
        # It is recommended that value be of type dict, str or list
        # Other types will come back differently to the way they go in (e.g. tuple->list, float->str)
        params = {'k': k, 'value': self.to_redis_value(value)}
        res = requests.put(self.base_url + '/state/' + self.write_key, params=params)
        if res.status_code == 200:
            return res.json()

    @staticmethod
    def to_redis_value(value):
        """ Used by MicroStateWriter prior to storage in redis database """
        # This may change if we move to using JSON redis module
        if ValueConventions.is_valid_value(value):
            return value
        elif isinstance(value, (list,dict,tuple)):
            if ValueConventions.has_nan(value):
                raise Exception('Values with NaN cannot be stored, sorry')
            else:
                try:
                    return json.dumps(value)
                except Exception as e:
                    raise Exception('Value cannot be JSON dumped so cannot be stored '+str(e) )

    @staticmethod
    def from_redis_value(value):
        """ Used by MicroStateWriter to infer a Python type """
        # Note: will not try to convert string back to int or float.
        # If you wish to preserve type then make it dict, tuple or list
        try:
            native = json.loads(value)
            if isinstance(native, (dict,list,tuple)):
                return native
            else:
                return value
        except Exception as e:
            return value

    def get_errors(self):
        """ Retrieve private log information """
        res = requests.get(self.base_url + '/errors/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

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

    def put_balance(self, source_write_key, amount=100.):
        """ Transfer some balance into self.write_key by reducing balance of source_write_key """
        res = requests.put(self.base_url + '/balance/' + self.write_key,
                           data={"source_write_key": source_write_key, "amount": amount})
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

    def bolster_balance_by_mining(self, seconds=1):
        """ For a short time, try to burn a MUID to bolster flagging balance """
        key = self.maybe_create_key(difficulty=10, seconds=max(seconds, 3))
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
        COMMON = ['set', 'submit']
        return [c for c in self.get_confirms() if
                c.get('operation') not in COMMON]  # TODO: Move strings like 'withdraw' to microconventions

    def get_withdrawals(self):
        """ Get withdrawal confirmations """
        return [c for c in self.get_confirms() if
                c.get('operation') == 'withdraw']  # TODO: Move strings like 'withdraw' to microconventions

    def get_cancellations(self):
        """ Get cancellation confirmations, which can occur long after withdrawal requests """
        return [c for c in self.get_confirms() if c.get('operation') == 'cancel']

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
        last_confirm_time = confirms[0].get("epoch_time")
        return time.time() - last_confirm_time

    def get_transactions(self, with_epoch=True):
        """
            :param with_timestamps bool     Set true to include epoch time (datetime already comes)
        """
        res = requests.get(self.base_url + '/transactions/' + self.write_key)
        if res.status_code == 200:
            transactions = res.json()
            transaction_values = [t[1] for t in transactions]
            if with_epoch:
                transaction_epoch_times = [int(t[0].split('-')[0]) / 1000 for t in transactions]
                for tv, tt in zip(transaction_values, transaction_epoch_times):
                    tv.update({'epoch_time': tt})
            return transaction_values
        else:
            raise Exception('Failed for ' + self.write_key)

    def get_elapsed_since_transaction(self):
        transactions = self.get_transactions(with_epoch=True)
        if not transactions:
            return None
        last_transaction_time = transactions[0].get("epoch_time")
        return time.time() - last_transaction_time

    def get_active(self, throw=False):
        try:
            res = requests.get(self.base_url + '/active/' + self.write_key)
            if res.status_code == 200:
                return res.json()
            elif throw:
                raise Exception('get_active() failed for ' + self.write_key)
        except requests.exceptions.ConnectionError as e:
            # Slightly more expensive operation. Very occasionally fails if internet isn't the greatest
            if throw:
                raise e
            else:
                print('WARNING: Failed to retrieve active ' + str(e))

    def get_performance(self, throw=False):
        try:
            res = requests.get(self.base_url + '/performance/' + self.write_key)
            if res.status_code == 200:
                return res.json()
            else:
                raise Exception('Failed for ' + self.write_key)
        except requests.exceptions.ConnectionError as e:
            # Slightly more expensive operation. Very occasionally fails if internet isn't the greatest
            if throw:
                raise e
            else:
                print('WARNING: Failed to retrieve active ' + str(e))

    def delete_performance(self):
        res = requests.delete(self.base_url + '/performance/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def submit(self, name, values, delay, verbose=True):
        """ Submit prediction scenarios
        :param name:      str         Examples:    cop.json   z1~cop.json   z2~cop~qp.json
        :param write_key: str         Example:    "5263ee89-e34e-44dc-8b91-445b302b043e"
        :param values:    [ float ]
        :return: bool
        """
        verbose = verbose or self.verbose
        if delay is None:
            delay = self.DELAYS[0]
            print(
                'It is suggested that you supply delay parameter to submit. Defaulting to shortest horizon but this will be removed in the future',
                flush=True)

        assert len(values) == self.num_predictions,'Wrong number of values submitted. Should be '+str(self.num_predictions)

        comma_sep_values = ",".join([str(v) for v in values])
        res = requests.put(self.base_url + '/submit/' + name,
                           data={'delay': delay, 'write_key': self.write_key, 'values': comma_sep_values})
        if res.status_code == 200:
            return res.json() if verbose else True
        elif res.status_code == 403:
            return False
        else:
            print('--- SUBMIT ERRORS ---- ')
            rrs = self.get_errors()[:2]
            pprint.pprint(rrs)
            print('', flush=True)
            raise Exception('Failed to submit')

    def submit_copula(self, name, prctls:[[float]], delay, verbose=True):
        """ Offers an alternative way to submit to copula streams.
               prctls: [ [p1,p2,p3] ]   list of percentile vectors in [0,1]^n , where n=2 or 3
        """
        assert '~' in name, "This method is intended for implied copula submission"
        values = [ self.to_zcurve(prctls=prctl) for prctl in prctls ]
        return self.submit(name=name, values=values, delay=delay, verbose=verbose)

    def submit_zvalues(self, name, zvalues: [[float]], delay, verbose=True):
        """ Offers an alternative way to submit to copula streams.
               prctls: [ [z1,z2,z3] ]   list of percentile vectors in [0,1]^n , where n=2 or 3
        """
        assert 'z2~' in name or 'z3~' in name, "This method is intended for implied copula submission"

        def squish(zs):
            prtcls = [ self.normcdf(z) for z in zs ]
            return self.to_zcurve(prctls=prtcls)

        values = sorted( [squish(zs) for zs in zvalues] )
        return self.submit(name=name, values=values, delay=delay, verbose=verbose)

    def cancel(self, name, delay=None, delays=None):
        """ Send request to cancel scenarios. However predictions won't be deleted immediately.

            :param  name    str
            :param  delay   int   or
            :param  delays [int]
            :returns bool

        """
        if delays is None and delay is None:
            delays = self.DELAYS
        elif delays is None:
            delays = [delay]
        codes = list()
        for delay in delays:
            res = requests.delete(self.base_url + '/submit/' + name,
                                  params={'write_key': self.write_key, 'delay': delay})
            codes.append(res.status_code)

        success = all([c == 200 for c in codes])
        operating = all([c in [200, 403] for c in codes])
        if not operating:
            raise Exception('Failed to cancel.')
        else:
            return success

    def active_performance(self, reverse=False, performance=None, active=None):
        performance = performance or self.get_performance()
        active = active or self.get_active()
        return OrderedDict(
            sorted([(horizon, balance) for horizon, balance in performance.items() if horizon in active],
                   key=lambda e: e[1], reverse=reverse))

    def worst_active_horizons(self, stop_loss, performance=None, active=None):
        """ Return horizons where we are losing more than stop_loss """
        return [horizon for horizon, balance in
                self.active_performance(reverse=True, performance=performance, active=active).items() if
                balance < -stop_loss]

    def cancel_worst_active(self, stop_loss, num=1000, performance=None, active=None):
        horizons = self.worst_active_horizons(stop_loss=stop_loss, performance=performance, active=active)[:num]
        for horizon in horizons:
            name, delay = self.split_horizon_name(horizon)
            self.cancel(name=name, delays=[delay])
            print('Cancelled participation in ' + str(horizon), flush=True)
            time.sleep(0.1)
        return horizons

    def cancel_all(self):
        for horizon in self.get_active():
            name, delay = self.split_horizon_name(horizon)
            self.cancel(name=name, delays=[delay])
            time.sleep(0.5)
