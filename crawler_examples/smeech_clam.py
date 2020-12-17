from microprediction import SequentialStreamCrawler
from microprediction.config_private import SMEECH_CLAM

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

if __name__ == '__main__':
    crawler = SequentialStreamCrawler(write_key=SMEECH_CLAM, max_active=50, stop_loss=5)
    crawler.set_repository('https://github.com/microprediction/microprediction/blob/master/crawler_examples/smeech_clam.py')
    crawler.run()
