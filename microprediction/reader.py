from microconventions import MicroConventions, api_url
import requests, time, sys
from pprint import pprint
import numpy as np
import json
from typing import List, Tuple

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started reading historical data, and the like.


class MicroReader(MicroConventions):

    def __init__(self, base_url=None, **kwargs):
        """ Establish connection and adopt configuration parameters from site """
        super().__init__(base_url=base_url or api_url(), **kwargs)

    def fix_stream_name(self,name:str)->str:
        if len(name)<5 or name[-5:]!='.json':
            print('Stream names should end in .json')
            return name+'.json'
        else:
            return name

    def request_get_json(self, method, arg=None, data=None, throw=True):
        # TODO: Can remove this after microconventions>0.1.0
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

    def __repr__(self):
        return json.dumps({'base_url':self.base_url})

    def get(self, name, throw=True):
        return self.request_get_json(method='live', arg=name, throw=throw)

    def get_current_value(self, name, throw=True):
        name = self.fix_stream_name(name=name)
        return self.request_get_json(method='live', arg=name, throw=throw)

    def get_sponsors(self) -> dict:
        return self.get_streams_by_sponsor()

    def get_streams_by_sponsor(self):
        return self.request_get_json(method='sponsors')

    def get_budgets(self):
        return self.get_streams_by_budget()

    def get_streams_by_budget(self):
        return self.request_get_json(method='budgets')

    def get_streams(self) -> dict:
        return self.get_sponsors()

    def get_prizes(self) -> dict:
        return self.request_get_json(method='prizes')

    def get_stream_names(self) -> [str]:
        return [ name for name in self.get_streams() ]

    def get_summary(self, name):
        return self.request_get_json(method='live', arg='summary::' + name)
        # res = requests.get(self.base_url + '/live/summary::' + name)

    def get_lagged(self,name, count=1000):
        name = self.fix_stream_name(name=name)
        return self.request_get_json(method='lagged',arg=name, data={'count':count-1})

    def get_recent_lagged_values(self, name, seconds:int, count=2000 ):
        lagged = self.get_lagged(name=name, count=count)
        t_cutoff = time.time() - seconds
        lagged_values = [v for (t, v) in lagged if t > t_cutoff]
        return lagged_values

    def append_chrono(self, name, chrono:List[Tuple], seconds=24 * 60 * 60, count=2000):
        """ Splice existing collection of historical time-value pairs to recent history stored on server

            chrono:  [(t,v)] history of values, preferably in chronological ordering
            returns: [(t,v)] extended history to present
        """
        chrono = sorted( chrono )
        lagged = self.get_recent_lagged_values(name=name, seconds=seconds, count=count)
        if len(chrono):
            t_cutoff = max([ t for (t,v) in chrono])
        else:
            t_cutoff = 0
        lagged_new = sorted( [ (t,v) for (t,v) in lagged if t>1e-6+t_cutoff ] )
        return list(chrono)+list(lagged_new)

    def get_lagged_values_and_times(self, name, count=1000):
        """ Preferred method """
        name = self.fix_stream_name(name=name)
        lagged = self.get_lagged(name=name, count=count)
        try:
            lagged_values = [l[1] for l in lagged]
            lagged_times  = [l[0] for l in lagged]
        except TypeError:
            # Lagged may be missing
            return [], []

        return lagged_values, lagged_times

    def get_lagged_values(self, name:str, count:int=1000):
        """ Retrieve lagged values of a time series
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        name = self.fix_stream_name(name=name)
        lagged_values, lagged_times = self.get_lagged_values_and_times(name=name,count=count)
        return lagged_values

    def get_lagged_copulas(self, name:str, count:int=5000):
        """ Retrieve history of implied copulas in [0,1]^n
             returns [ [p1,p2,p3] ]
        """
        name = self.fix_stream_name(name=name)
        assert '~' in name,'This method is intended for copula streams'
        lagged_values, lagged_times = self.get_lagged_values_and_times(name=name, count=count)
        dim = 2 if 'z2~' in name else 3
        lagged_prctls = [ self.from_zcurve(zvalue,dim=dim) for zvalue in lagged_values ]
        return lagged_prctls

    def get_lagged_zvalues(self, name:str, count:int=5000):
        """ Retrieve history of implied z in [-inf,inf]^n
             returns [ [z1,z2,z3], [ , ,] ]
        """
        name = self.fix_stream_name(name=name)
        assert '~' in name, 'This method is intended for bivariate or trivariate copula streams'
        lagged_values, lagged_times = self.get_lagged_values_and_times(name=name, count=count)
        dim = 2 if 'z2~' in name else 3

        def expand(z):
            ps = self.from_zcurve(zvalue=z,dim=dim)
            return [ self.norminv(p) for p in ps ]

        lagged_zs = [ expand(z) for z in lagged_values]
        return lagged_zs


    def get_lagged_times(self, name:str, count:int=1000) -> list:
        """ Retrieve lagged times
        :param name:    cop.json   z1~cop.json   z2~cop~qp.json
        :return: [ float ]
        """
        name = self.fix_stream_name(name=name)
        lagged_values, lagged_times = self.get_lagged_values_and_times(name=name, count=count)
        return lagged_times

    def get_delayed_value(self, name: str, delay: int):
        """ Retrieve quarantined value.
            This is the most recent data point after going back at least delay seconds

            param: name    cop.json   z1~cop.json   z2~cop~qp.json
            param: delay
            :return: [ float ]
        """
        name = self.fix_stream_name(name=name)
        return self.request_get_json(method='live', arg='delayed::' + str(delay) + self.SEP + name)
        # res = requests.get(self.base_url + '/live/delayed::' + str(delay) + "::" + name)

    def get_repository(self, write_key):
        """ Get repository associated with a write key """
        # You can also supply a hash of the write key instead
        return self.request_get_json(method='repository', arg=write_key)
        # res = requests.get(self.base_url + '/repository/' + write_key)

    def get_predictions(self, write_key, name, delay:int, strip=True, consolidate=True):
        """ Retrieve predictions for a given horizon

              strip_percentiles  If false, returns dictionary with individual submissions
              consolidate        If false, returns tuples (owner,value)
                                 Otherwise just returns values

        """
        name = self.fix_stream_name(name=name)
        tickets = self.request_get_json(method='predictions', arg=name, data={"write_key":write_key,"delay":delay})
        if strip:
            tups = [(ticket.split('::')[1], val) for ticket, val in tickets.items()]
            if consolidate:
                return sorted([v for owner,v in tups])
            else:
                return tups
        else:
            return tickets

    def get_samples(self, write_key, name, delay:int, strip=True, consolidate=True):
        """ Retrieve samples for a given horizon (i.e. predictions that have left quarantine)

              strip_percentiles  If false, returns dictionary with individual submissions
              consolidate        If false, returns tuples (owner,value)
                                 Otherwise just returns values

        """
        name = self.fix_stream_name(name=name)
        tickets = self.request_get_json(method='samples', arg=name, data={"write_key":write_key,"delay":delay})
        if strip:
            tups = [(ticket.split('::')[1], val) for ticket, val in tickets.items()]
            if consolidate:
                return sorted([v for owner,v in tups])
            else:
                return tups
        else:
            return tickets


    def median(self, name: str, delay: int):
        name = self.fix_stream_name(name=name)
        return self.inv_cdf(name=name, delay=delay, p=0.5, num=15)

    def inv_cdf(self, name: str, delay: int, p=None, ps=None, num=25):
        """ Approximate PPF

             p    float  or
             ps  [float]
             num Number of interpolation points to use

        """
        name = self.fix_stream_name(name=name)
        # This won't choose x values based on the percentiles supplied, so it is a bit dumb in that sense
        cdf = self.get_cdf_lagged(name=name, delay=delay, num=num)
        ps_ = ps or [p]
        xs = np.interp(x=ps_, xp=cdf["x"], fp=cdf["y"], left=None, right=None)
        return list(xs) if ps is None else ps[0]

    def get_discrete_pdf_lagged(self, name: str, delay: int = None, num: int=25, lagged_values=None):
        """ Retrieve estimate of PDF ... only when discrete values are taken

                num   Maximum number of points to compute PDF at

        """
        if delay is None:
            delay = self.DELAYS[0]
        # PDF for continuous case is not implemented yet, sorry!
        lagged_values = lagged_values or self.get_lagged_values(name=name)
        values = self.cdf_values(lagged_values=lagged_values, num=num, as_discrete=True)
        raw_cdf = self._get_cdf(name=name, delay=delay, values=values)
        return {'x':raw_cdf['x'], 'y':self.discrete_pdf(raw_cdf['y'])} if raw_cdf.get('x') else raw_cdf

    def get_cdf_lagged(self, name: str, delay: int, num: int = 25, lagged_values=None, as_discrete=None):
        """ Get CDF using automatically selected x-values based on lags

              num:             Maximum number of points to use
              lagged_values:   Supply these to avoid an extra http round trip
              as_discrete      Supply bool if you know

        """
        lagged_values = lagged_values or self.get_lagged_values(name=name)
        if as_discrete is None:
            as_discrete = self.is_discrete(lagged_values=lagged_values, num=num, ndigits=12)
        values = self.cdf_values(lagged_values=lagged_values, num=num, as_discrete=as_discrete)
        raw_cdf = self._get_cdf(name=name, delay=delay, values=values)
        return self.discrete_cdf(raw_cdf) if as_discrete and raw_cdf.get('x') else raw_cdf

    def get_cdf(self, name: str, delay: int, values: [float], as_discrete=False) -> dict:
        """
            Get CDF using supplied x values
        """
        raw_cdf = self._get_cdf(name=name, delay=delay, values=values)
        return self.discrete_cdf(raw_cdf) if as_discrete and raw_cdf.get('x') else raw_cdf

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
        return self.evenly_spaced_percentiles(num=self.num_predictions)


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
