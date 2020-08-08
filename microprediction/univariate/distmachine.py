from microconventions.stats_conventions import StatsConventions


class DistMachine(object):

    # Base class for distribution fitting machines
    # SequentialStreamCrawler constructor expects a DistributionMachine
    # This is a state engine that has a ppf function

    def __init__(self):
        pass

    def update(self, value: float, dt=None, **ignored):
        pass

    def inv_cdf(self, p: float) -> float:
        return StatsConventions.norminv(p)



