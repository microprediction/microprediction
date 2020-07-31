from microprediction import MicroCrawler


class DiracCrawler(MicroCrawler):

    # Probably not the best idea

    def sample(self, lagged_values, **ignored):
        x = 0.5*lagged_values[0]+0.5*lagged_values[1]
        return [x]*self.num_predictions
