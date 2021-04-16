from microprediction.config_private import MALAXABLE_FOX
from microprediction import MicroCrawler
import numpy as np
from collections import Counter

# In version 0.16.2 the default crawler does something very similar to the following,
# so you don't actually need all this. It is here for reference
# See also Toastable Fox https://github.com/microprediction/microprediction/blob/master/crawler_examples/toastable_fox.py

# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com
# Need help? New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com


class EmpiricalTrafficAndElectricityCrawler(MicroCrawler):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def include_stream(self, name=None, **ignore):
        return ( 'traffic' in name or 'electricity' in name or 'sox' in name ) and not '~' in name

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
        change_spray = list(range(-150,150))
        values.extend(change_spray)
        values = values[:self.num_predictions]
        abs_values=[ lagged_values[0]+chg for chg in values ]
        return sorted(abs_values)


if __name__=='__main__':
    crawler = EmpiricalTrafficAndElectricityCrawler(write_key=MALAXABLE_FOX, stop_loss=15, max_active=150, min_lags=100)
    crawler.set_repository('https://github.com/microprediction/microprediction/blob/master/crawler_tutorial/empirical_traffic_changes.py')
    crawler.run()