from microprediction.fitcrawler import FitCrawler
from microprediction.univariate.expnormdist import ExpNormDist
from microprediction.config_private import EXHALABLE_CAT

if __name__ == '__main__':
    crawler = FitCrawler(write_key=EXHALABLE_CAT, machine_type=ExpNormDist, max_evals=3, min_seconds=6, min_elapsed=5*60, max_active=50)
    crawler.set_repository(url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/exhalable_cat.py')
    crawler.run()
