from microprediction import MicroWriter
import time

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started creating streams.


class PandasLoop(MicroWriter):

    # Creates multiple streams by looping over rows of a pandas dataframe
    # One column per stream.
    # Column names should be value stream names

    def __init__(self, df, interval, write_key, origin, with_copulas=False, verbose=False):
        """
        :param df:            pd.DataFrame   row names become stream names
        :param interval:
        :param write_key:
        :param origin:
        :param func_args:
        """
        assert self._valid_size(df),' Invalid size '
        assert self._valid_names(df), ' Invalid column name for stream '
        self.df           = df
        self.origin       = origin           # Epoch time for start of loop
        self.interval     = interval         # Minutes between each update
        self.with_copulas = with_copulas
        self.verbose = verbose
        super().__init__(write_key=write_key)

    def __repr__(self):
        return self.df.__repr__()

    def _valid_size(self,df):
        return len(df.index)>10000 and len(df.columns)<=10

    def _fix_name(self,name):
        return name+'.json' if '.json' not in name else name

    def _valid_names(self,df):
        return all( self.is_valid_name(name=name+'.json') for name in list(df.columns))

    def names(self):
        return [ self._fix_name( name ) for name in list(self.df.columns) ]

    def _values(self, k):
        """ Return k'th row of the dataset as a vector """
        return list(self.df.iloc[[k]]._values[0])

    def _current_row(self):
        """ Which row is it appropriate to sample from right now?
            :returns int
        """
        return int( self._intervals() % len(self.df.index) )

    def current_values(self):
        k = self._current_row()
        return self._values(k)

    def _intervals(self):
        """ Count fractional units of time, corresponding to a row number, since self.origin """
        return (time.time() - self.origin) / (self.interval * 60)

    def wait_until_no_race_condition(self):
        """ Delay until we are not near the boundary of an interval """
        while abs(self._intervals() % 1) < 0.05:
            time.sleep(1)
            print('Waiting to avoid race condition')
        print('Okay we are good to go')

    def publish(self):
        names = self.names()
        values = self.current_values()
        if self.with_copulas:
            return self.cset(names=names, values=values)
        else:
            res = list()
            for name, value in zip(names, values):
                try:
                    res.append( self.set(name=name,value=value) )
                    if self.verbose:
                        print({'name':name,'value':value})
                except Exception as e:
                    print(str(e))
                    error_msg = 'Could not set '+name+' to value='+str(value) + str(e)
                    print(error_msg)
                    res.append(0)
            if self.verbose:
                print(' ', flush=True)
            return res

    def run(self,minutes=60):
        loop_start = time.time()
        self.wait_until_no_race_condition()

        st = time.time()
        while time.time()<loop_start+60*minutes:
            res = self.publish()
            self.publish_callback(res)
            et = time.time()
            sleep_time = ( (st-et) % (60*self.interval))
            print('Sleeping for '+str(sleep_time)+' seconds.')
            time.sleep(sleep_time)

    def publish_callback(self,res):
        """ In case you want to do something with publishing results """
        pass
