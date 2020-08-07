from microprediction.univariate.distributionmachine import DistributionMachine
from tdigest import TDigest


class DigestMachine(DistributionMachine):

    # Default for SequentialStreamCrawler

    def __init__(self):
        super().__init__()
        self.digest = TDigest()

    def update(self, value, dt=None, **ignored):
        self.digest.update(value)

    def inv_cdf(self, p):
        return self.digest.percentile(100. * p)
