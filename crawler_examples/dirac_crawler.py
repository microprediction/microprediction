from microprediction import MicroCrawler

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

class DiracCrawler(MicroCrawler):

    # Probably not the best idea

    def sample(self, lagged_values, **ignored):
        x = 0.5*lagged_values[0]+0.5*lagged_values[1]
        return [x]*self.num_predictions
