from microprediction.univariate.distmachine import DistMachine
from tdigest import TDigest


class DigestDist(DistMachine):

    # Default DistMachine used in the SequentialStreamCrawler
    # This has no params

    def __init__(self, state: TDigest = None, params=None):
        state = state or TDigest()
        super().__init__(state=state, params=params)

    def update(self, value=None, dt=None, **kwargs):
        if value is not None:
            self.state.update(value)

    def inv_cdf(self, p):
        return self.state.percentile(100. * p)
