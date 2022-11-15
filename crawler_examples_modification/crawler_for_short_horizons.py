from microprediction import MicroCrawler
try:
    from microprediction.config_private import SOSHED_BOA as WRITE_KEY
except ImportError:
    WRITE_KEY = None


# Crawler submitting predictions for only the 1 and 5 minute horizons, not the 15 minute and 1hr ones.
# (Requires us to create a new class, using the standard boilerplate for __init__)
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


class MyCrawler(MicroCrawler):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def include_delay(self, delay=None, name=None, **ignore):
        return delay<=self.DELAYS[1]


if __name__=='__main__':
    mw = MyCrawler(write_key=WRITE_KEY)
    mw.run()