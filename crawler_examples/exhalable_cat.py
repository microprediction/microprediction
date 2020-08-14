from microprediction.config_private import EXHALABLE_CAT
from microprediction import SequentialStreamCrawler
from microprediction.univariate.digestdist import DigestDist


class ShrinkingDigestDist(DigestDist):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def inv_cdf(self, p):
        """ Sprays just a little less """
        q = 0.9 * p + 0.1 * 0.5
        return super().inv_cdf(100. * q)


if __name__ == "__main__":
    print('starting',flush=True)
    crawler = SequentialStreamCrawler(write_key=EXHALABLE_CAT, min_lags=500, max_active=50,
                                      machine_type=DigestDist)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/exhalable_cat.py')
    crawler.min_lags = 500
    crawler.run()
