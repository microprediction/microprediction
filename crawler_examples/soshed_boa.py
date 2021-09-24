from microprediction import MicroCrawler
import numpy as np
from statsmodels.tsa.ar_model import AutoReg, ar_select_order

from microprediction.config_private import SOSHED_BOA  # <--- You'll need your own key instead


# You can create a private key using this colab notebook
# https://github.com/microprediction/microprediction/blob/master/notebook_examples/New_Key.ipynb

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com


class MyCrawler(MicroCrawler):

    def __init__(self, write_key):
        super().__init__(stop_loss=3.0, min_lags=50, sleep_time=15 * 60, write_key=write_key, quietude=1, verbose=False)

    def exclude_stream(self, name=None, **ignore):
        """ Only participate in continuous streams """
        try:
            ex = self.excluded_already
        except AttributeError:
            self.excluded_already = list()

        if name in self.excluded_already:
            return True
        else:
            try:
                lagged_values = self.get_lagged_values(name=name)
                uniques = np.unique(lagged_values)
                is_discrete = len(uniques) < 0.2 * len(lagged_values)
                if is_discrete:
                    self.excluded_already.append(name)
                    return True
            except Exception as e:
                print('Something odd with '+name)
                print(str(e))
                return True

    def sample(self, lagged_values, lagged_times=None, **ignored):
        """ Find Unique Values to see if outcomes are discrete or continuous """
        rev_values = lagged_values[::-1]  # our data are in reverse order, the AR model needs the opposite
        ARmodel = ar_select_order(rev_values, maxlag=int(0.1 * len(rev_values)))
        model_fit = ARmodel.model.fit()
        point_est = model_fit.predict(start=len(rev_values), end=len(rev_values), dynamic=False)[0]
        st_dev = np.std(rev_values)
        ps = self.evenly_spaced_percentiles(self.num_predictions)
        vs = [ point_est + st_dev*self.norminv(p) for p in ps]
        jiggle = 0.2*abs(vs[114]-vs[113])*np.random.rand()
        v_jiggled = [ v+jiggle for v in vs ]
        return v_jiggled


if __name__ == "__main__":
    crawler = MyCrawler(write_key=SOSHED_BOA)
    crawler.set_repository(
        url='https://github.com//microprediction/microprediction/blob/master/crawler_examples/soshed_boa.py') # <--- Optionally include a link to your repo.
    crawler.set_email("no_email@supplied.com")  # <--- Put your email here. Only used to send you a voucher if you win a daily prize
    crawler.run(withdraw_all=True)
