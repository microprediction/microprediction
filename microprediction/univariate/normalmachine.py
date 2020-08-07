from microprediction.univariate.distributionmachine import DistributionMachine
from microconventions.stats_conventions import StatsConventions
import math

# Very simple example of an online Normal Distribution estimator
# https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Welford's_online_algorithm

def _safe_sqrt(x):
    return math.sqrt(x) if x > 0 else 0


class NormalMachine(DistributionMachine):

    def __init__(self):
        super().__init__()
        self.count = 0
        self.mean  = 0
        self.M2    = 0

    def __repr__(self):
        return 'mean='+str(self.mean)+',var='+str(math.sqrt(self.var()))

    def var(self):
        return self.M2 / (self.count-1) if self.count > 1 else 0

    def pvar(self):
        return self.M2 / self.count if self.count > 0 else 0

    def update(self, value, dt=None, **ignored):
        self.count += 1
        delta = value - self.mean
        self.mean += delta / self.count
        delta2 = value - self.mean
        self.M2 += delta * delta2

    def inv_cdf(self, p):
        return self.mean + StatsConventions.norminv(p) * self.var()
