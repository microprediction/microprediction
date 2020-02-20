import requests

NUM_PREDICTIONS=1000
DELAY=70

class Collider(object):
    # Minimalist client for scenario submissions and lagged value retrieval
    # Go to https://algorithmia.com/algorithms/threezaemails/Register to obtain a write_key

    def __init__(self,base_url="http://www.microprediction.com/collider/",write_key="invalid_key"):
        self.base_url = base_url
        self.write_key = write_key

    def get_lagged_values(self, name):
        """ Retrieve lagged values of a time series
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        res = requests.get(self.base_url+'/'+name )
        if res.status_code==200:
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
        res = requests.put(self.base_url + name, data={'delay':DELAY, 'write_key': self.write_key, 'values': comma_sep_values})
        return res.status_code

    def withdraw(self,name):
        res = requests.delete(self.base_url + name, params={'delay':DELAY} )
        return res.status_code
