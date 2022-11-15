from microprediction import MicroCrawler
try:
    from microprediction.config_private import SOSHED_BOA as WRITE_KEY
except ImportError:
    WRITE_KEY = None


# Crawler submitting to streams with a known sponsor only.
# (Requires us to create a new class, using the standard boilerplate for __init__)
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


SPONSOR_CODES = ["fa76039a2e11ed1f7d5d2cfef240455d", "e3b1055033076108b4279c473cde3a67"]
# (Examples from https://www.microprediction.com/competitions/daily, reads "Fathom Gazelle")


class MyCrawler(MicroCrawler):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def include_sponsor(self, sponsor=None, **ignore):
        """
            Receives a sponsor public key (not the private one, which you don't know)
            Should return boolean
        """
        return sponsor in SPONSOR_CODES


if __name__=='__main__':
    mw = MyCrawler(write_key=WRITE_KEY)
    mw.run()