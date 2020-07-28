from microconventions import MicroConventions, api_url
import requests, time, sys
from pprint import pprint
import numpy as np


class MicroReader(MicroConventions):

    def __init__(self,base_url=None, **kwargs):
        """ Establish connection and adopt configuration parameters from site """
        super().__init__(base_url=base_url or api_url(),**kwargs)

    def get(self, name):
        res = requests.get(self.base_url + '/live/' + name)
        if res.status_code == 200:
           return res.json()

    def get_current_value(self, name):
        res = requests.get(self.base_url + '/live/' + name)
        if res.status_code == 200:
           return float(res.json())

    def get_leaderboard(self, name, delay=None):
        res = requests.get(self.base_url + '/leaderboards/' + name, data={"delay": delay})
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def get_overall(self):
        res = requests.get(self.base_url + '/overall/')
        if res.status_code == 200:
            performance = res.json()
        else:
            raise Exception('Failed for ' + self.write_key)

    def get_sponsors(self):
        res = requests.get(self.base_url + '/sponsors')
        if res.status_code == 200:
            return res.json()

    def get_streams(self):
        return self.get_sponsors()

    def get_budgets(self):
        res = requests.get(self.base_url + '/budgets')
        if res.status_code == 200:
            return res.json()

    def get_summary(self, name):
        res = requests.get(self.base_url + '/live/summary::' + name)
        if res.status_code == 200:
            return res.json()

    def get_lagged_values(self, name):
        """ Retrieve lagged values of a time series
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        res = requests.get(self.base_url+'/live/lagged_values::'+name )
        if res.status_code==200:
            return res.json()

    def get_lagged_times(self, name):
        """ Retrieve lagged times
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        res = requests.get(self.base_url+'/live/lagged_times::'+name )
        if res.status_code==200:
            return res.json()

    def get_delayed_value(self, name, delay=None):
        """ Retrieve quarantined value
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        delay = delay or self.DELAYS[0]
        res = requests.get(self.base_url + '/live/delayed::'+str(delay)+ "::" + name)
        if res.status_code == 200:
            return res.json()

    def get_repository(self, write_key):
        """ Get repository associated with a write key """
        # You can also supply a hash of the write key instead
        res = requests.get(self.base_url + '/repository/' + write_key)
        if res.status_code == 200:
            return res.json()

    def inv_cdf(self, name, delay=None, p=0.5):
        """ Approximate interpolation of value, defaulting to median"""
        cdf = self.get_cdf(name=name, delay=delay)
        x = np.interp(p=p, xp=cdf["x"], fp=cdf["y"], left=None, right=None)
        return x


    def get_cdf(self, name, delay=None, values=None):
        if delay is None:
            delay = self.DELAYS[0]
        if values is None:  # Supply x-values at which approximate crowd cdf will be computed. # FIXME... should not be here an also in conventions
            values = [-2.3263478740408408, -1.6368267885518997, -1.330561513178897, -1.1146510149326596,
                      -0.941074530352976, -0.792046894425591, -0.6588376927361878, -0.5364223812298266,
                      -0.4215776353171568, -0.3120533220328322, -0.20615905948527324, -0.10253336200497987, 0.0,
                      0.10253336200497973, 0.20615905948527324, 0.31205332203283237, 0.4215776353171568,
                      0.5364223812298264, 0.6588376927361878, 0.7920468944255913, 0.941074530352976, 1.1146510149326592,
                      1.330561513178897, 1.6368267885519001, 2.3263478740408408]
        comma_sep_values = ",".join([str(v) for v in values])
        res = requests.get(self.base_url + '/cdf/' + name, params={"values": comma_sep_values})
        if res.status_code == 200:
            return res.json()

    # For convenience...
    # This will move to microconventions

    def percentiles(self):
        """
           :returns  [ float ]   A list of 225 evenly spaced numbers in (0,1)
        """
        return list(np.linspace(start=1 / (2 * self.num_predictions), stop=1 - 1 / (2 * self.num_predictions), num=self.num_predictions))


class MicroReaderStatus(MicroReader):

     def __init__(self):
         super().__init__()

     def reader_status(self):
         examples = {  'get': {'name': 'cop.json'},
                       'get_current_value': {'name': 'cop.json'},
                       'get_sponsors': {},
                       'get_streams': {},
                       'get_budgets': {},
                       'get_summary': {'name': 'cop.json'},
                       'get_lagged_values': {'name': 'cop.json'},
                       'get_lagged_times': {'name': 'cop.json'},
                       'get_delayed_value': {'name': 'cop.json'},
                       'get_cdf': {'name': 'cop.json'}
                     }
         report = list()
         for method, kwargs in examples.items():
             call_time = time.time()
             try:
                 data = self.__getattribute__(method)(**kwargs)
                 sz = sys.getsizeof(data)
                 st = 'up' if sz>0 else ''
                 tm = time.time() - call_time
                 er = ''
             except Exception as e:
                 st = 'down'
                 tm = -1
                 er = str(e)
                 sz = -1
             report.append((method, st, tm, er, sz))
         return report


if __name__=="__main__":
    pprint(MicroReaderStatus().reader_status())