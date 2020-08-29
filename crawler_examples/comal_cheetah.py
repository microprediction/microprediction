from microprediction.fitcrawler import FitCrawler
from microprediction.univariate.expnormdist import ExpNormDist
from microprediction.config_private import COMAL_CHEETAH

if __name__ == '__main__':
    crawler = FitCrawler(write_key=COMAL_CHEETAH, machine_type=ExpNormDist, max_evals=15, min_seconds=30, min_elapsed=60*60, max_active=25)
    crawler.delete_performance()
    crawler.set_repository(url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/comal_cheetah.py')
    crawler.run()
