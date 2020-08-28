from microprediction import SequentialStreamCrawler
from microprediction.config_private import FLOATABLE_BEE
from microprediction.univariate.processes import is_process
from microprediction.univariate.digestdist import DigestDist

# Illustrates deriving from SequentialStreamCrawler

# This creates a crawler that sometimes handles noisy processes better because
# it "floats" ... moving slowly through observations rather than chasing the last one.
# (this example is also supposed to demonstrate how you might combine a point estimate
# with an existing distributional estimate. Soon there will be a simpler way to do this)


class FloatingCrawler(SequentialStreamCrawler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stickiness = 0.25

    def include_stream(self, name=None, **ignore):
        """ Only attempt regular streams that seem to be processes """
        if '~' in name:
            return False
        else:
            lagged_values = self.get_lagged_values(name=name)
            return is_process(lagged_values)

    def initial_state(self, name, lagged_values, lagged_times, **machine_params):
        """ Simple moving average """
        state = super().initial_state(name=name, lagged_values=lagged_values, lagged_times=lagged_times, **machine_params)
        state['anchor'] = lagged_values[0]
        return state

    def update_state(self, state, lagged_values=None, lagged_times=None, **ignore):
        """ Use existing distributional update, but move the anchor slowly """
        state = super().update_state(state=state, lagged_values=lagged_values, lagged_times=lagged_times, **ignore)
        state['anchor'] = self.stickiness * state['anchor'] + (1 - self.stickiness) * lagged_values[0]
        return state

    def sample_using_state(self, state, lagged_values, lagged_times, name, delay, **ignored):
        """ By default samples are centered around the last value. Center them on anchor instead. """
        samples = super().sample_using_state(state=state, lagged_values=lagged_values, lagged_times=lagged_times,
                                             name=name, delay=delay, **ignored)
        offset = state['anchor'] - lagged_values[0]
        return [s + offset for s in samples]


if __name__ == '__main__':
    crawler = FloatingCrawler(write_key=FLOATABLE_BEE, machine_type=DigestDist, min_lags=500, max_active=100)
    crawler.run()
