from microprediction import MicroCrawler
try:
    from microprediction.config_private import SOSHED_BOA as WRITE_KEY
except ImportError:
    WRITE_KEY = None


QUIETUDE = 1000  # Only 1:1000 chance of producing stdout


if __name__=='__main__':
    mw = MicroCrawler(write_key=WRITE_KEY, quietude=QUIETUDE)
    mw.run()