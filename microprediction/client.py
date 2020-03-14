from microprediction.conventions import MicroConventions
import requests, muid

class MicroReader(MicroConventions):

    def __init__(self,base_url=None):
        """ Establish connection and adopt configuration parameters from site """
        self.base_url = base_url or "http://www.microprediction.com/"
        config = requests.get(self.base_url+"/config.json").json()
        self.delays = config["delays"]
        self.num_predictions = config["num_predictions"]

    def get(self, name):
        res = requests.get(self.base_url + '/live/' + name)
        if res.status_code == 200:
           return res.json()

    def get_current_value(self, name):
        res = requests.get(self.base_url + '/live/' + name)
        if res.status_code == 200:
           return float(res.json())

    def get_summary(self, name):
        res = requests.get(self.base_url + '/live/summary::' + name)
        if res.status_code == 200:
            return res.json()

    def get_lagged_values(self, name):
        """ Retrieve lagged values of a time series
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        res = requests.get(self.base_url+'live/lagged_values::'+name )
        if res.status_code==200:
            return res.json()

    def get_lagged_times(self, name):
        """ Retrieve lagged times
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        res = requests.get(self.base_url+'live/lagged_times::'+name )
        if res.status_code==200:
            return res.json()

    def get_delayed_value(self, name, delay=None):
        """ Retrieve quarantined value
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        delay = delay or self.delays[0]
        res = requests.get(self.base_url + 'live/delayed::'+str(delay)+ "::" + name)
        if res.status_code == 200:
            return res.json()

    def get_cdf(self, name, values=None):
        if values is None:  # Supply x-values at which approximate crowd cdf will be computed.
            values = [-2.3263478740408408, -1.6368267885518997, -1.330561513178897, -1.1146510149326596,
                      -0.941074530352976, -0.792046894425591, -0.6588376927361878, -0.5364223812298266,
                      -0.4215776353171568, -0.3120533220328322, -0.20615905948527324, -0.10253336200497987, 0.0,
                      0.10253336200497973, 0.20615905948527324, 0.31205332203283237, 0.4215776353171568,
                      0.5364223812298264, 0.6588376927361878, 0.7920468944255913, 0.941074530352976, 1.1146510149326592,
                      1.330561513178897, 1.6368267885519001, 2.3263478740408408]
        comma_sep_values = ",".join([str(v) for v in values])
        res = requests.get(self.base_url + 'live/' + name, params={"values", comma_sep_values})
        if res.status_code == 200:
            return res.json()

class MicroWriter(MicroReader):

    def __init__(self, write_key="invalid_key", base_url="http://www.microprediction.com/"):
        """ Create the ability to write """
        super().__init__(base_url=base_url)
        assert muid.mverify(write_key), "Invalid write_key. Mine one at muid.org. "
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

    def withdraw(self, name ):
        """ Withdraw predictions """
        codes = list()
        for delay in self.delays:
            res = requests.delete(self.base_url + 'submit/'+name, params={'delay':delay} )
            codes.append(res.status_code)
        return all([ c==200 for c in codes ] )
