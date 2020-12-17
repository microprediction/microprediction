from microprediction.config_private import MESOLE_MAMMAL
from microprediction.sequentialcrawler import SequentialStreamCrawler
from microprediction.univariate.skewdist import SkewDist

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

if __name__ == "__main__":
    crawler = SequentialStreamCrawler(write_key=MESOLE_MAMMAL, min_lags=20, machine_type=SkewDist)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/mesole_mammal.py')
    crawler.min_lags = 50
    crawler.max_active = 50
    crawler.run()