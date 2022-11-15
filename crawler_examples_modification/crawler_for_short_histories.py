from microprediction import MicroCrawler
try:
    from microprediction.config_private import SOSHED_BOA as WRITE_KEY
except ImportError:
    WRITE_KEY = None


# Allow crawler to participate in streams even if the history is quite short
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


MIN_LAGS = 5


if __name__=='__main__':
    mw = MicroCrawler(write_key=WRITE_KEY, min_lags=MIN_LAGS)
    mw.run()