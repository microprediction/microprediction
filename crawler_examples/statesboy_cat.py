# Illustrates use of SequentialStreamCrawler
# Yes, yet another way to skin the cat

from microprediction.config_private import STATESBOY_CAT
from tdigest import TDigest
from microprediction import SequentialStreamCrawler, DistMachine


class DigestMachine(DistMachine):

    def __init__(self):
        super().__init__()
        self.digest = TDigest()

    def update(self, value, dt=None, **kwargs):
        self.digest.update(value)

    def inv_cdf(self, p):
        return self.digest.percentile(100. * p)


if __name__ == "__main__":
    crawler = SequentialStreamCrawler(write_key=STATESBOY_CAT, min_lags=500, machine_type=DigestMachine)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/statesboy_cat.py')
    crawler.min_lags = 500
    crawler.run()
