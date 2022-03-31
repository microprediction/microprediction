from microprediction import MicroCrawler
try:
    from microprediction.config_private import SOSHED_BOA as WRITE_KEY
except ImportError:
    WRITE_KEY = None


# Provides more stdout


if __name__=='__main__':
    mw = MicroCrawler(write_key=WRITE_KEY, verbose=True)
    mw.run()