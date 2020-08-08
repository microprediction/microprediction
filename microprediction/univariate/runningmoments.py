import math
import json

# Online moment estimators
# https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Welford's_online_algorithm


class RunningVariance(object):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # So it can be used as mixin
        self.count = 0
        self.mean = 0
        self.M2 = 0

    def __repr__(self):
        return json.dumps({'mean':self.mean, 'var':math.sqrt(self.var())})

    def std(self):
        v = self.var()
        return math.sqrt(v) if v > 0 else 0

    def var(self):
        """ Sample variance """
        return self.M2 / (self.count - 1) if self.count > 1 else 0

    def pvar(self):
        """ Population variance """
        return self.M2 / self.count if self.count > 0 else 0

    def update(self, value, dt=None, **ignored):
        self.count += 1
        delta = value - self.mean
        self.mean += delta / self.count
        delta2 = value - self.mean
        self.M2 += delta * delta2


class RunningKurtosis(RunningVariance):

    def __init__(self):
        super().__init__()
        self.M3 = 0
        self.M4 = 0

    def __repr__(self):
        properties = json.loads( super().__repr__() )
        properties.update( {'skewness':self.skewness(),'kurtosis':self.kurtosis()})
        return json.dumps(properties)

    def update(self, value, dt=None, **ignored):
        n1 = self.count
        self.count = self.count + 1
        delta = value - self.mean
        delta_n = delta / self.count
        delta_n2 = delta_n * delta_n
        term1 = delta * delta_n * n1
        self.mean = self.mean + delta_n
        self.M4 = self.M4 + term1 * delta_n2 * (
                self.count * self.count - 3 * self.count + 3) + 6 * delta_n2 * self.M2 - 4 * delta_n * self.M3
        self.M3 = self.M3 + term1 * delta_n * (self.count - 2) - 3 * delta_n * self.M2
        self.M2 = self.M2 + term1

    def kurtosis(self):
        return (self.count * self.M4) / (self.M2 * self.M2) - 3

    def skewness(self):
        return self.M3 / self.M2
