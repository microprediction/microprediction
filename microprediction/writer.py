from microprediction.reader import MicroReader
import muid, requests

class MicroWriter(MicroReader):

    def __init__(self, write_key="invalid_key", base_url="http://www.microprediction.com/"):
        """ Create the ability to write """
        super().__init__(base_url=base_url)
        assert muid.validate(write_key), "Invalid write_key. Mine one at muid.org. "
        self.write_key = write_key

    def __repr__(self):
        return {'write_key':self.write_key,"animal":muid.animal(self.write_key)}

    def set(self, name, value):
        """ Create or update a stream """
        res = requests.put(self.base_url + '/live/' + name, data={"write_key": self.write_key, "value": value})
        if res.status_code == 200:
            return float(res)

    def get_errors(self):
        """ Retrieve private log information """
        res = requests.get(self.base_url + 'live/errors::' + self.write_key)
        if res.status_code == 200:
            return res.json()

    def submit(self, name, values):
        """ Submit prediction scenarios
        :param name:      str         Examples:    cop.json   z1~cop.json   z2~cop~qp.json
        :param write_key: str         Example:    "5263ee89-e34e-44dc-8b91-445b302b043e"
        :param values:    [ float ]
        :return: bool
        """
        assert len(values)==self.num_predictions
        comma_sep_values = ",".join([ str(v) for v in values ] )
        res = requests.put(self.base_url + 'submit/' + name, data={'delay':self.delays[0], 'write_key': self.write_key, 'values': comma_sep_values})
        return res.status_code==200

    def cancel(self, name):
        """ Withdraw scenarios """
        codes = list()
        for delay in self.delays:
            res = requests.delete(self.base_url + 'submit/'+name, params={'delay':delay} )
            codes.append(res.status_code)
        return all([ c==200 for c in codes ] )
