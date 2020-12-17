from microprediction.fitcrawler import FitCrawler
from microprediction.univariate.expnormdist import ExpNormDist
from microprediction.config_private import ALBAHACA_MOLE

# Need help? New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com


class ShortOnlyCrawler(FitCrawler):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def exclude_stream(self, name=None, **ignore):
        # Fit crawler poorly suited for non-process TS
        return 'emoji' in name

    def include_delay(self, delay, name=None, **ignore):
        return delay<700


if __name__ == '__main__':
    crawler = ShortOnlyCrawler(write_key=ALBAHACA_MOLE, machine_type=ExpNormDist, max_evals=10,
                         min_seconds=20, min_elapsed=60 * 60, max_active=150, decay=0.005)
    crawler.delete_performance()
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/albahaca_mole.py')
    crawler.run()


