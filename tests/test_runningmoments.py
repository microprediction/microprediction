from microprediction.univariate.runningmoments import RunningVariance, RunningKurtosis
import numpy as np
from statistics import variance, pvariance
from scipy.stats import kurtosis, skew


# Check against creme


def test_normal_against_creme():
    try:
        from creme.preprocessing import StandardScaler
        xs = list(np.random.randn(100))
        machine = RunningVariance()
        scalar = StandardScaler()
        for x in xs:
            machine.update(value=x)
            scalar.fit_one({'x': x})
        var1 = np.var(xs)
        var2 = machine.var()
        var3 = variance(xs)
        var4 = pvariance(xs)
        var5 = scalar.vars['x']
        var6 = machine.pvar()
        print([var1, var2, var3, var4, var5, var6])
        assert abs(var2 - var3) < 0.0001
        assert abs(var5 - var1) < 0.0001
        assert abs(var5 - var6) < 0.0001
    except ImportError:
        pass

def test_normal():
    xs = list(np.random.randn(100))
    machine = RunningVariance()
    for x in xs:
        machine.update(value=x)
    var1 = np.var(xs)
    var2 = machine.var()
    var3 = variance(xs)
    var4 = pvariance(xs)
    var6 = machine.pvar()
    print([var1, var2, var3, var4, var6])
    assert abs(var2 - var3) < 0.0001


def test_kurtosis():
    xs = list(np.random.randn(200))
    machine = RunningKurtosis()
    for x in xs:
        machine.update(value=x)

    k1 = machine.kurtosis()
    k2 = kurtosis(xs, fisher=True)
    k3 = kurtosis(xs, fisher=False)

    assert (abs(k1 - k2) < 0.0001)

    s1 = machine.skewness()
    s2 = skew(xs, bias=False)
    s3 = skew(xs, bias=True)

    assert (abs(s1 - s2) < 0.06)
