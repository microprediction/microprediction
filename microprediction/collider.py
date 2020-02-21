import requests

NUM_PREDICTIONS=1000
DELAY=70

class Collider(object):
    # Minimalist client for scenario contest submission management and stream data
    # Go to https://algorithmia.com/algorithms/threezaemails/Register to obtain a write_key

    def __init__(self,base_url="http://www.microprediction.com/",write_key="invalid_key"):
        self.base_url = base_url
        self.write_key = write_key

    def set(self, name, write_key, value):
        res = requests.put(self.base_url + '/streams/' + name, data={"write_key":write_key,"value":value})
        if res.status_code == 200:
            return float(res)

    def get(self, name):
        res = requests.get(self.base_url + '/streams/' + name)
        if res.status_code == 200:
           return res.json()

    def get_current_value(self, name):
        res = requests.get(self.base_url + '/streams/' + name)
        if res.status_code == 200:
           return float(res.json())

    def get_lagged_values(self, name):
        """ Retrieve lagged values of a time series
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        res = requests.get(self.base_url+'streams/lagged_values::'+name )
        if res.status_code==200:
            return res.json()

    def get_lagged_times(self, name):
        """ Retrieve lagged times
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        res = requests.get(self.base_url+'streams/lagged_times::'+name )
        if res.status_code==200:
            return res.json()

    def get_delayed_value(self, name):
        """ Retrieve quarantined value
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        res = requests.get(self.base_url + 'streams/delayed::'+str(DELAY)+ "::" + name)
        if res.status_code == 200:
            return res.json()

    def get_errors(self):
        res = requests.get(self.base_url + 'streams/errors::' + self.write_key)
        if res.status_code == 200:
            return res.json()

    def get_balance(self):
        res = requests.get(self.base_url + 'streams/errors::' + self.write_key)
        if res.status_code == 200:
            return res.json()

    def submit(self, name, values):
        """ Submit prediction scenarios
        :param name:      str         Examples:    cop.json   z1~cop.json   z2~cop~qp.json
        :param write_key: str         Example:    "5263ee89-e34e-44dc-8b91-445b302b043e"
        :param values:    [ float ]
        :return:
        """
        assert len(values)==NUM_PREDICTIONS
        comma_sep_values = ",".join([ str(v) for v in values ] )
        res = requests.put(self.base_url + 'scenarios/' + name, data={'delay':DELAY, 'write_key': self.write_key, 'values': comma_sep_values})
        return res.status_code==200

    def withdraw(self, name ):
        res = requests.delete(self.base_url + 'scenarios/'+name, params={'delay':DELAY} )
        return res.status_code==200
