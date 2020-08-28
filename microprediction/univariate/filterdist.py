from abc import ABC
from microprediction.univariate.distmachine import LikeDist
import typing


class FilterDist(LikeDist, ABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    ###############################################################
    #  Shouldn't need to mess with the rest unless you want to    #
    ###############################################################

    def likelihood(self, values: [float], dts: typing.Optional[list], initial_state=None):
        saved_state = self.state
        self.state = initial_state
        if dts is None:
            dts = [ None for value in values ]
        for value, dt in zip( values, dts):
            state = self.update(value=value, dt=dt)






class ExampleFilterDist(FilterDist):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)