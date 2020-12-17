from microprediction.config_private import TOASTABLE_FOX
from microprediction import MicroCrawler

# Toastable Fox runs the default crawler.
# It ain't terrible.

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

if __name__=='__main__':
    crawler = MicroCrawler(write_key=TOASTABLE_FOX)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/toastable_fox.py')
    crawler.max_active = 500
    crawler.run()