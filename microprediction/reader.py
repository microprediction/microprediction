from microconventions import MicroConventions, api_url
import requests, time, sys
from pprint import pprint
import numpy as np
from microprediction.univariate.cdfvalues import evenly_spaced_percentiles, cdf_values, is_discrete, discrete_cdf, discrete_pdf


class MicroReader(MicroConventions):

    def __init__(self, base_url=None, **kwargs):
        """ Establish connection and adopt configuration parameters from site """
        super().__init__(base_url=base_url or api_url(), **kwargs)

    def request_get_json(self, method, arg=None, data=None, throw=True):
        try:
            if data is not None:
                res = requests.get(self.base_url + '/' + method + '/' + arg, data=data)
            elif arg is not None:
                res = requests.get(self.base_url + '/' + method + '/' + arg)
            elif data is None and arg is None:
                res = requests.get(self.base_url + '/' + method)
            if res.status_code == 200:
                return res.json()
        except ConnectionError as e:
            print('WARNING: ConnectionError attempting to get ' + method)
            if throw:
                raise e

    def get(self, name, throw=True):
        return self.request_get_json(method='live', arg=name, throw=throw)

    def get_current_value(self, name, throw=True):
        return self.request_get_json(method='live', arg=name, throw=throw)

    def get_leaderboard(self, name, delay=None, throw=True):
        return self.request_get_json(method='leaderboards', arg=name, data={"delay": delay}, throw=throw)
        # res = requests.get(self.base_url + '/leaderboards/' + name, data={"delay": delay})

    def get_overall(self):
        return self.request_get_json(method='overall')

    def get_sponsors(self):
        return self.request_get_json(method='sponsors')

    def get_streams(self):
        return self.get_sponsors()

    def get_budgets(self):
        return self.request_get_json(method='budgets')

    def get_summary(self, name):
        return self.request_get_json(method='live', arg='summary::' + name)
        # res = requests.get(self.base_url + '/live/summary::' + name)

    def get_lagged_values(self, name):
        """ Retrieve lagged values of a time series
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        return self.request_get_json(method='live', arg='lagged_values::' + name)
        # res = requests.get(self.base_url + '/live/lagged_values::' + name)

    def get_lagged_times(self, name):
        """ Retrieve lagged times
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        return self.request_get_json(method='live', arg='lagged_times::' + name)
        # res = requests.get(self.base_url + '/live/lagged_times::' + name)

    def get_delayed_value(self, name: str, delay: int):
        """ Retrieve quarantined value.
            This is the most recent data point after going back at least delay seconds

            param: name    cop.json   z1~cop.json   z2~cop~qp.json
            param: delay
            :return: [ float ]
        """
        return self.request_get_json(method='live', arg='delayed::' + str(delay) + self.SEP + name)
        # res = requests.get(self.base_url + '/live/delayed::' + str(delay) + "::" + name)

    def get_repository(self, write_key):
        """ Get repository associated with a write key """
        # You can also supply a hash of the write key instead
        return self.request_get_json(method='repository', arg=write_key)
        # res = requests.get(self.base_url + '/repository/' + write_key)

    def median(self, name: str, delay: int):
        return self.inv_cdf(name=name, delay=delay, p=0.5, num=15)

    def inv_cdf(self, name: str, delay: int, p=None, ps=None, num=25):
        """ Approximate PPF

             p    float  or
             ps  [float]
             num Number of interpolation points to use

        """
        # This won't choose x values based on the percentiles supplied, so it is a bit dumb in that sense
        cdf = self.get_cdf_lagged(name=name, delay=delay, num=num)
        ps_ = ps or [p]
        xs = np.interp(x=ps_, xp=cdf["x"], fp=cdf["y"], left=None, right=None)
        return list(xs) if ps is None else ps[0]

    def get_discrete_pdf_lagged(self, name: str, delay: int = 25, num: int=25, lagged_values=None):
        """ Retrieve estimate of PDF ... only when discrete values are taken

                num   Maximum number of points to compute PDF at

        """
        # PDF for continuous case is not implemented yet, sorry!
        lagged_values = lagged_values or self.get_lagged_values(name=name)
        values = cdf_values(lagged_values=lagged_values, num=num, as_discrete=True)
        raw_cdf = self._get_cdf(name=name, delay=delay, values=values)
        return {'x':raw_cdf['x'], 'y':discrete_pdf(raw_cdf['y'])}

    def get_cdf_lagged(self, name: str, delay: int, num: int = 25, lagged_values=None, as_discrete=None):
        """ Get CDF using automatically selected x-values based on lags

              num:             Maximum number of points to use
              lagged_values:   Supply these to avoid an extra http round trip
              as_discrete      Supply bool if you know

        """
        lagged_values = lagged_values or self.get_lagged_values(name=name)
        if as_discrete is None:
            as_discrete = is_discrete(lagged_values=lagged_values, num=num, ndigits=12)
        values = cdf_values(lagged_values=lagged_values, num=num, as_discrete=as_discrete)
        raw_cdf = self._get_cdf(name=name, delay=delay, values=values)
        return discrete_cdf(raw_cdf) if as_discrete else raw_cdf

    def get_cdf(self, name: str, delay: int, values: [float], as_discrete=False) -> dict:
        """
            Get CDF using supplied x values
        """
        raw_cdf = self._get_cdf(name=name, delay=delay, values=values)
        return discrete_cdf(raw_cdf) if as_discrete else raw_cdf

    def _get_cdf(self, name: str, delay: int, values: [float]) -> dict:
        """ Implements approximate cumulative distribution function based on community micropredictions

              values  A list of x-values at which CDF will be evaluated
              Returns dict   {'x':[ float ], 'y':[ float ]}  where

            This cdf can be tricky to interpret
        """
        comma_sep_values = ",".join([str(v) for v in sorted(values)])
        return self.request_get_json(method='cdf', arg=name, data={'delay': delay, 'values': comma_sep_values})
        # res = requests.get(self.base_url + '/cdf/' + name, params={"delay":delay,"values": comma_sep_values})

    # For convenience...
    # This will move to microconventions

    def percentiles(self) -> [float]:
        """ A list of 225 evenly spaced numbers in (0,1) """
        return evenly_spaced_percentiles(num=self.num_predictions)


class MicroReaderStatus(MicroReader):

    def __init__(self):
        super().__init__()

    def reader_status(self):
        examples = {'get': {'name': 'cop.json'},
                    'get_current_value': {'name': 'cop.json'},
                    'get_sponsors': {},
                    'get_streams': {},
                    'get_budgets': {},
                    'get_summary': {'name': 'cop.json'},
                    'get_lagged_values': {'name': 'cop.json'},
                    'get_lagged_times': {'name': 'cop.json'},
                    'get_delayed_value': {'name': 'cop.json','delay':self.DELAYS[2]},
                    'get_cdf': {'name': 'cop.json','delay':self.DELAYS[2],'values':[-1,0,1]}
                    }
        report = list()
        for method, kwargs in examples.items():
            call_time = time.time()
            try:
                data = self.__getattribute__(method)(**kwargs)
                sz = sys.getsizeof(data)
                st = 'up' if sz > 0 else ''
                tm = time.time() - call_time
                er = ''
            except Exception as e:
                st = 'down'
                tm = -1
                er = str(e)
                sz = -1
            report.append((method, st, tm, er, sz))
        return report


if __name__ == "__main__":
    pprint(MicroReaderStatus().reader_status())
