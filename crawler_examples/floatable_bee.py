from microprediction import SequentialStreamCrawler
from microprediction.config_private import FLOATABLE_BEE
from microprediction.fitcrawler import FitCrawler
from microprediction.univariate.expnormdist import ExpNormDist
from copy import deepcopy

# Floatable Bee uses on-the-fly fitting only, and does not try to
# use stored parameters. It is set to ony run for 35 streams.
# This consumes around 20,000 cpu seconds per month.

# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com
# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com


class ShortOnlyCrawler(FitCrawler):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def exclude_stream(self, name=None, **ignore):
        # Fit crawler poorly suited for non-process TS
        return 'emoji' in name or 'die' in name or 'coin' in name

    def include_delay(self, delay, name=None, **ignore):
        return delay<700

DEFAULT_EXPNORM_PARAMS = {'g1': 0.5, 'g2': 5.0, 'logK': -2., 'loc': 0.0, 'logScale': 0.0}
DEFAULT_EXPNORM_LOWER = {'g1': 0.001, 'g2': 0.001, 'logK': -5, 'loc': -0.15, 'logScale': -4}
DEFAULT_EXPNORM_UPPER = {'g1': 1.0, 'g2': 15.0, 'logK': 1, 'loc': 0.15, 'logScale': 4.0}
DEFAULT_EXPNORM_HYPER = {'lower_bounds': deepcopy(DEFAULT_EXPNORM_LOWER),
                         'upper_bounds': deepcopy(DEFAULT_EXPNORM_UPPER),
                         'space': None, 'algo': None, 'max_evals': 11}

if __name__ == '__main__':
    crawler = ShortOnlyCrawler(write_key=FLOATABLE_BEE, machine_type=ExpNormDist, max_evals=200,
                         min_seconds=20, min_elapsed=24*60*60, max_active=35, decay=0.01)
    crawler.delete_performance()
    crawler.hyper_params = DEFAULT_EXPNORM_HYPER
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/floatable_bee.py')
    crawler.set_email("no_email@supplied.com")  # Only used to send you a voucher if you win a daily prize
    crawler.run()

