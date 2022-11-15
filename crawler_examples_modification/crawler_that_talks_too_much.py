from microprediction import MicroCrawler
try:
    from microprediction.config_private import SOSHED_BOA as WRITE_KEY
except ImportError:
    WRITE_KEY = None


# Provides more stdout
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


if __name__=='__main__':
    mw = MicroCrawler(write_key=WRITE_KEY, verbose=True)
    mw.run()