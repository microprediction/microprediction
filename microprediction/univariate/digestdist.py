from microprediction.univariate.distmachine import DistMachine
from tdigest import TDigest


class DigestDist(DistMachine):

    # Default DistMachine used in the SequentialStreamCrawler

    def __init__(self):
        super().__init__()
        self.digest = TDigest()

    def update(self, value, dt=None, **ignored):
        self.digest.update(value)

    def inv_cdf(self, p):
        return self.digest.percentile(100. * p)
