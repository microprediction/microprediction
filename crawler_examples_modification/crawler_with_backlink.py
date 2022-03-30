from microprediction import MicroCrawler
try:
    from microprediction.config_private import SOSHED_BOA as WRITE_KEY
except ImportError:
    WRITE_KEY = None


# Crawler with a CODE badge
# See https://www.microprediction.org/leaderboard.html for how this looks

URL_YOU_WANT_ON_LEADERBOARD = "https://github.com/microprediction/microprediction/blob/master/crawler_examples/bedabble_toad.py"


if __name__=='__main__':
    mw = MicroCrawler(write_key=WRITE_KEY)
    mw.set_repository(url=URL_YOU_WANT_ON_LEADERBOARD)
    mw.run()