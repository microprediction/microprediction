from microprediction import MicroCrawler
try:
    from microprediction.config_private import SOSHED_BOA as WRITE_KEY
except ImportError:
    WRITE_KEY = None


# Crawler with an associated email
# (This is required to qualify for https://www.microprediction.com/competitions/daily)
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


EMAIL = "pcotton@intechnvestments.com"

if __name__=='__main__':
    mw = MicroCrawler(write_key=WRITE_KEY)
    mw.set_email(email=EMAIL)
    mw.run()