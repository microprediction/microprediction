from credentials import ALFLAT_SLOTH
from tdigest import TDigest
from microprediction import SequentialStreamCrawler, DistMachine

# Crawler that goes after sector streams

class DigestMachine(DistMachine):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.digest = TDigest()

    def include_stream(self, name=None, **ignore):
        return 'rdps' in name

    def update(self, value, dt=None, **kwargs):
        self.digest.update(value)

    def inv_cdf(self, p):
        return self.digest.percentile(100. * p)


if __name__ == "__main__":
    crawler = SequentialStreamCrawler(write_key=ALFLAT_SLOTH, min_lags=500, machine_type=DigestMachine, max_active=200)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/aflat_sloth.py')
    crawler.min_lags = 500
    crawler.run()
