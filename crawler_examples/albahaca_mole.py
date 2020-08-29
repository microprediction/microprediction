from microprediction.fitcrawler import FitCrawler
from microprediction.univariate.expnormdist import ExpNormDist
from microprediction.config_private import ALBAHACA_MOLE


if __name__ == '__main__':
    crawler = FitCrawler(write_key=ALBAHACA_MOLE, machine_type=ExpNormDist, max_evals=20, min_seconds=20, min_elapsed=60, max_active=20)
    crawler.delete_performance()
    crawler.set_repository(url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/albahaca_mole.py')
    crawler.run()
