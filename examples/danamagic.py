MY_MUID = '1bb1d1c184b68d7dc29a220746eecebf'
from microprediction import MicroCrawler
import numpy as np
from statsmodels.tsa.ar_model import AutoReg




class MyCrawler(MicroCrawler):

    def __init__(self,write_key):
        super().__init__(stop_loss=1.0,min_lags=20,sleep_time=15*60,write_key=write_key,quietude=1,verbose=False)

    # create a difference transform of the dataset
    def difference(self,dataset):
    	diff = list()
    	for i in range(1, len(dataset)):
    		value = dataset[i] - dataset[i - 1]
    		diff.append(value)
    	return np.array(diff)

    # Make a prediction give regression coefficients and lag obs
    def predict(self, coef, history):
    	yhat = coef[0]
    	for i in range(1, len(coef)):
    		yhat += coef[i] * history[-i]
    	return yhat

    #def exclude_stream(self, name=None, **ignore):
    #    NAUGHTY =  ['three_body', 'badminton', 'pandemic']
    #    return any( name in n for n in NAUGHTY)

    def candidate_streams(self):
        bad_names = ['three_body', 'badminton', 'pandemic']
        good_names = []
        candidate_names = [name for name, sponsor in self.get_sponsors().items() if name[:1] != 'z' ] #exclude z streams

        # not_bad_candidates = [ name for name in candidate_names if not any(name in n for n in bad_names) ]

        for cname in candidate_names:
            okay = True
            for bname in bad_names:
                if bname in cname:
                    okay = False
                    break
            if okay == True:
                good_names.append(cname)
        return good_names

    def sample(self, lagged_values, lagged_times=None, **ignored ):
        """ Find Unique Values to see if outcomes are discrete or continuous """
        uniques = np.unique(lagged_values)
        if len(uniques) < 0.3*len(lagged_values): #arbitrary cutoff of 30% to determine whether outcomes are continuous or quantized
            v = [s for s in (np.random.choice(lagged_values, self.num_predictions))] #randomly select from the lagged values and return as answer
        else:

            """ Simple Autoregression """
            X = self.difference(lagged_values)
            model = AutoReg(X, lags=6)
            model_fit = model.fit()
            coef = model_fit.params
            point_est = self.predict(coef, lagged_values)
            st_dev = np.std(lagged_values)
            v = [s for s in (np.random.normal(point_est, st_dev, self.num_predictions))]

        return sorted(v)


if __name__=="__main__":
    mw = MyCrawler(write_key=MY_MUID)
    mw.run()
