from microprediction.fitcrawler import FitCrawler
from microprediction.univariate.expnormdist import ExpNormDist
from microprediction.config_private import BEDABBLE_TOAD

if __name__ == '__main__':
    crawler = FitCrawler(write_key=BEDABBLE_TOAD, machine_type=ExpNormDist, max_evals=7, min_seconds=15, min_elapsed=60, max_active=50)
    crawler.set_repository(url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/bedabble_toad.py')
    crawler.run()
