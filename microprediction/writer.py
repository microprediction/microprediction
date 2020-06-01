from microprediction.reader import MicroReader, default_url
import muid, requests, pprint

class MicroWriter(MicroReader):

    def __init__(self, write_key="invalid_key", base_url=None, verbose=True, **kwargs ):
        """ Create the ability to write """
        super().__init__(base_url=base_url or default_url(),**kwargs)
        string_write_key = write_key if isinstance(write_key,str) else write_key.decode()
        assert muid.validate(string_write_key), "Invalid write_key. Mine one at muid.org. "
        self.write_key = string_write_key
        self.verbose   = verbose

    def __repr__(self):
        return {'write_key':self.write_key,"animal":muid.animal(self.write_key)}

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

    def get_balance(self):
        res = requests.get(self.base_url + '/balance/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def put_balance(self, source_write_key, amount=100. ):
        """ Transfer some balance into self.write_key """
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
        key = self.maybe_create_key(difficulty=12,seconds=seconds)
        if key is not None:
            self.put_balance(source_write_key=key)
            return key

    def restore_balance_by_mining(self, difficulty=12):
        """ Mine a MUID and deposit it to bring the balance up from a negative number """
        source_write_key = self.create_key(difficulty=difficulty)
        return self.put_balance(source_write_key=source_write_key)

    def get_confirms(self):
        res = requests.get(self.base_url + '/confirms/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def get_leaderboard(self,name,delay=None):
        res = requests.patch(self.base_url + '/leaderboard/' + name, data={"delay": delay})
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def get_overall(self):
        res = requests.patch(self.base_url + '/overall/')
        if res.status_code == 200:
            performance = res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

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

    def submit(self, name, values, delay=None, verbose=None):
        """ Submit prediction scenarios
        :param name:      str         Examples:    cop.json   z1~cop.json   z2~cop~qp.json
        :param write_key: str         Example:    "5263ee89-e34e-44dc-8b91-445b302b043e"
        :param values:    [ float ]
        :return: bool
        """
        verbose = verbose or self.verbose
        delay = delay or self.delays[0]
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

    def cancel(self, name, delays=None):
        """ Withdraw scenarios """
        codes = list()
        delays = delays or self.delays
        for delay in delays:
            res = requests.delete(self.base_url + '/submit/'+name, params={'write_key':self.write_key,'delay':delay} )
            codes.append(res.status_code)

        success   = all([ c==200 for c in codes ] )
        operating = all([ c in [200,403] for c in codes])
        if not operating:
            raise Exception('Failed to cancel.')
        else:
            return success
