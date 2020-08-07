from microprediction import NormalMachine
import numpy as np
from statistics import variance, pvariance

def test_normal():
    xs = list(np.random.randn(100))
    machine = NormalMachine()
    for x in xs:
        machine.update(value=x)
    var1 = np.var(xs)
    var2 = machine.var()
    var3 = variance(xs)
    var4 = pvariance(xs)
    print([var1,var2,var3,var4])
    assert abs(var2-var3)<0.0001