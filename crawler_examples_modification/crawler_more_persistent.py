from microprediction import MicroCrawler
try:
    from microprediction.config_private import SOSHED_BOA as WRITE_KEY
except ImportError:
    WRITE_KEY = None


# Allow crawler to lose a large number of credits on a given horizon, but not give up
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


STOP_LOSS = 100


if __name__=='__main__':
    mw = MicroCrawler(write_key=WRITE_KEY, stop_loss=STOP_LOSS)
    mw.run()