try:
    from credentials import EXACTABLE_FOX as WRITE_KEY
except ImportError:
    raise Exception('You will need a write key. See https://www.microprediction.com/private-keys')

# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com
# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


if __name__ == "__main__":

    try:
        from echochamber import EchoCrawler

        class Fox(EchoCrawler):

            def include_stream(self, name, **ignore):
                """ continuous data only please """
                lagged_values = self.get_lagged_values(name)
                return len(lagged_values) > 500 and len(set(lagged_values)) > 100

            def exclude_stream(self, name, **ignore):
                """ No derived streams """
                return '~' in name

    except ImportError:
        print('pip install echochamber')

    crawler = Fox(write_key=WRITE_KEY)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/exactable_fox.py')
    crawler.set_email("no_email@supplied.com")  # Only used to send you a voucher if you win a daily prize
    crawler.max_active = 500
    crawler.run()
