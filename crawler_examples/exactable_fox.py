from microprediction.config_private import EXACTABLE_FOX

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

# This guy uses

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

    crawler = Fox(write_key=EXACTABLE_FOX)
    crawler.set_repository(
        url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/exactable_fox.py')
    crawler.max_active = 500
    crawler.run()
