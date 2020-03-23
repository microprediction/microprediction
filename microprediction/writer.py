from microprediction.reader import MicroReader
import muid, requests, pprint

class MicroWriter(MicroReader):

    def __init__(self, write_key="invalid_key", base_url="http://www.microprediction.com", verbose=True ):
        """ Create the ability to write """
        super().__init__(base_url=base_url)
        string_write_key = write_key if isinstance(write_key,str) else write_key.decode()
        assert muid.validate(string_write_key), "Invalid write_key. Mine one at muid.org. "
        self.write_key = string_write_key
        self.verbose   = verbose

    def __repr__(self):
        return {'write_key':self.write_key,"animal":muid.animal(self.write_key)}

    def set(self, name, value):
        """ Create or update a stream """
        res = requests.put(self.base_url + '/live/' + name, data={"write_key": self.write_key, "value": value})
        if res.status_code ==200:
            return float(res)
        else:
            err = self.get_errors()
            pprint.pprint(err)
            print('',flush=True)
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

    def get_confirms(self):
        res = requests.get(self.base_url + '/confirms/' + self.write_key)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def submit(self, name, values, delay=None):
        """ Submit prediction scenarios
        :param name:      str         Examples:    cop.json   z1~cop.json   z2~cop~qp.json
        :param write_key: str         Example:    "5263ee89-e34e-44dc-8b91-445b302b043e"
        :param values:    [ float ]
        :return: bool
        """
        delay = delay or self.delays[0]
        assert len(values)==self.num_predictions

        comma_sep_values = ",".join([ str(v) for v in values ] )
        res = requests.put(self.base_url + '/submit/' + name, data={'delay':self.delays[0], 'write_key': self.write_key, 'values': comma_sep_values})
        if res.status_code==200:
            if self.verbose:
                confirms = self.get_confirms()
                errors = self.get_errors()
                pprint.pprint(confirms[:2])
                pprint.pprint(errors[:2])
                print('',flush=True)
                return True
        elif res.status_code==403:
            return False
        else:
            rrs = self.get_errors()
            pprint.pprint(rrs)
            print('',flush=True )
            raise Exception('Failed to submit')

    def cancel(self, name):
        """ Withdraw scenarios """
        codes = list()
        for delay in self.delays:
            res = requests.delete(self.base_url + '/submit/'+name, params={'delay':delay} )
            codes.append(res.status_code)
        success   = all([ c==200 for c in codes ] )
        operating = all([ c in [200,403] for c in codes])
        if not operating:
            raise Exception('Failed to cancel.')
        else:
            return success
