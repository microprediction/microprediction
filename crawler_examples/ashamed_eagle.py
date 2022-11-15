try:
    from credentials import ASHAMED_EAGLE as WRITE_KEY
except ImportError:
    raise Exception('You will need a write key. See https://www.microprediction.com/private-keys')

from microprediction import MicroCrawler
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

# Forked from a crawler by Dan Carroll
# ARIMA and Normal sampling.


# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com
# And see the crawling docs: https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html


class MyCrawler(MicroCrawler):

    def __init__(self, **kwargs):
        super().__init__( **kwargs)

    def exclude_stream(self, name=None, **ignore):
        return '~' in name


    # evaluate an ARIMA model for a given order (p,d,q)
    def evaluate_arima_model(self, X, arima_order):
        # prepare training dataset
        train_size = int(len(X) * 0.66)
        train, test = X[0:train_size], X[train_size:]
        history = [x for x in train]
        # make predictions
        predictions = list()
        for t in range(len(test)):
            model = ARIMA(history, order=arima_order)
            model_fit = model.fit()
            yhat = model_fit.forecast()[0]
            predictions.append(yhat)
            history.append(test[t])
        # calculate out of sample error
        error = mean_squared_error(test, predictions)
        return error

    # evaluate combinations of p, d and q values for an ARIMA model
    def evaluate_models(self, dataset, p_values, d_values, q_values):
        # dataset = dataset.astype('float32')
        best_score, best_cfg = float("inf"), (0, 0, 0)
        for p in p_values:
            for d in d_values:
                for q in q_values:
                    order = (p, d, q)
                    try:
                        mse = self.evaluate_arima_model(dataset, order)
                        if mse < best_score:
                            best_score, best_cfg = mse, order
                    except:
                        continue
        return best_cfg

    def sample(self, lagged_values, lagged_times=None, **ignored):
        """ Find Unique Values to see if outcomes are discrete or continuous """
        uniques = np.unique(lagged_values)
        chronological_values = lagged_values[::-1]
        if len(uniques) < 0.3 * len(
                lagged_values):  # arbitrary cutoff of 30% to determine whether outcomes are continuous or quantized
            v = [s for s in (np.random.choice(lagged_values,
                                              self.num_predictions))]  # randomly select from the lagged values and return as answer
        else:

            """ Simple ARIMA """
            # evaluate parameters
            p_values = [0, 1, 2, 4, 6, 8, 10]  # these are kind of arbitrary, but need to put a limit on it
            d_values = range(0, 3)  # arbitrary, but need to put a limit on it
            q_values = range(0, 3)  # arbitrary, but need to put a limit on it
            best_order = self.evaluate_models(chronological_values, p_values, d_values, q_values)
            arma_mod = ARIMA(lagged_values, order=best_order, trend='n')
            model_fit = arma_mod.fit()
            point_est = model_fit.predict(len(lagged_values), len(lagged_values), dynamic=True)
            st_dev = np.std(lagged_values)
            v = [s for s in (np.random.normal(point_est, st_dev, self.num_predictions))]
                  # See also microprediction.samplers for other ways to do the last part

        return sorted(v)


if __name__ == "__main__":
    mw = MyCrawler(write_key=WRITE_KEY,min_lags=50, quietude=1, verbose=False)
    mw.set_repository(
        url='https://github.com//microprediction/microprediction/blob/master/crawler_examples/ashamed_eagle.py')
    mw.run(withdraw_all=False)
