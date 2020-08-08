from microprediction.univariate.distmachine import DistMachine
from microconventions.stats_conventions import StatsConventions
from microprediction.univariate.runningmoments import RunningVariance


# Maintain running estimate of normal distribution

class NormalDist(RunningVariance, DistMachine):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def inv_cdf(self, p: float) -> float:
        return self.mean + StatsConventions.norminv(p) * self.std()

