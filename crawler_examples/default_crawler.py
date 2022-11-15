from microprediction import MicroCrawler

# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com
# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


if __name__ == '__main__':
    crawler = MicroCrawler()
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/default_crawler.py')
    crawler.set_email("no_email@supplied.com")  # Only used to send you a voucher if you win a daily prize
    crawler.run()
