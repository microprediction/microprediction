try:
    from microprediction.config_private import TOASTABLE_FOX
except ImportError:
    raise Exception('You will need a write key. See https://www.microprediction.com/private-keys')
from microprediction import MicroCrawler

# Toastable Fox runs the default crawler.
# It ain't terrible.

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

if __name__=='__main__':
    crawler = MicroCrawler(write_key=TOASTABLE_FOX)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/toastable_fox.py')
    crawler.set_email("no_email@supplied.com")  # Only used to send you a voucher if you win a daily prize
    crawler.max_active = 500
    crawler.run()
