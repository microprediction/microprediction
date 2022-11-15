from microprediction.config_private import EXHALABLE_CAT
from microprediction.fitcrawler import FitCrawler
from microprediction.univariate.expnormdist import ExpNormDist


# Illustrates the use of offline parameter estimation
# See the repo  microprediction/offline for how to use Github actions for this purpose
# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


STORED_PARAM_URL = 'https://raw.githubusercontent.com/microprediction/offline/main/modelfits/expnorm'


class RegularFitCrawler(FitCrawler):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def include_stream(self, name=None, **ignore):
        return '~' not in name


if __name__ == '__main__':
    crawler = RegularFitCrawler(write_key=EXHALABLE_CAT, machine_type=ExpNormDist, max_evals=50,
                         min_seconds=1, min_elapsed=60*60, max_active=500, decay=0.005,
                         param_base_url=STORED_PARAM_URL, stop_loss=50)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/exhalable_cat.py')
    crawler.set_email("no_email@supplied.com")  # Only used to send you a voucher if you win a daily prize
    crawler.run()


