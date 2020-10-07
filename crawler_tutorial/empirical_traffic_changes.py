from microprediction import MicroCrawler
import numpy as np
from collections import Counter


class EmpiricalTrafficCrawler(MicroCrawler):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def include_stream(self, name=None, **ignore):
        return 'traffic-nj511' in name and not '~' in name

    def exclude_delay(self, delay, name=None, **ignore):
        return delay>50000  # Lower this to have any effect

    def sample(self, lagged_values, lagged_times=None, name=None, delay=None, **ignored):
        """ Must return a list of 225 numbers """
        changes = np.diff(list(reversed(lagged_values)),n=4)
        counter = dict(Counter(changes))
        d = dict(counter)
        num_total = len(changes)
        d1 = dict([ (change,round(225*change_count/num_total)) for change, change_count in d.items()])
        values = list()
        for change, rounded_count in d1.items():
            values.extend( [change]*rounded_count )
        change_spray = list(range(-50,50))
        values.extend(change_spray)
        values = values[:self.num_predictions]
        abs_values=[ lagged_values[0]+chg for chg in values ]
        return sorted(abs_values)


if __name__=='__main__':
    try:
        from microprediction.config_private import COSTOTOME_BOA
        crawler = EmpiricalTrafficCrawler(write_key=COSTOTOME_BOA,stop_loss=5, max_active=15, min_lags=100)
        crawler.run()
    except ImportError:
        print('You need a write_key. I''m making one for you now. ')
        from microprediction import new_key
        print(new_key(difficulty=11))