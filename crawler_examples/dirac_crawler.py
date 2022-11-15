from microprediction import MicroCrawler

# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com
# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


class DiracCrawler(MicroCrawler):

    # Probably not the best idea !

    def sample(self, lagged_values, **ignored):
        x = 0.5*lagged_values[0]+0.5*lagged_values[1]
        return [x]*self.num_predictions
