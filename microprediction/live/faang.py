import numpy as np
import os
import json
import math
from itertools import combinations_with_replacement
from microprediction.live.iex import iex_latest_prices
from microprediction import MicroReader
from scipy.stats import kurtosis

# A few conventions used by FAANG streams


FAANG_TICKERS = ['fb', 'aapl', 'amzn', 'nflx', 'googl']
FAANG_NAMES = ['faang_' + str(k) + '.json' for k,ticker in enumerate(FAANG_TICKERS)] # Stream names
N_FAANG = len(FAANG_TICKERS)
FAANG_COMBINATIONS = list(combinations_with_replacement(range(N_FAANG), r=5))


def iex_scaled_log_faang(api_key:str):
    """
       Retrieve live prices for FAANG and transform
       api_key: An IEX api key
    """
    sp = iex_latest_prices(tickers=FAANG_TICKERS, api_key=api_key)
    return [1000 * math.log(v) for v in sp]


def portfolio_from_combination(c):
    """
       Converts a combination like 1,1,1,2,3 into weighted portfolio
    """
    n = len(c)
    w = 0.5*np.ones(n)/n
    for ndx in c:
        w[ndx]+=0.5/n
    return w


def readable_portfolio_from_combination(c,tickers):
    w = portfolio_from_combination(c)
    return 'Portfolio comprising '+', '.join( [ str(round(wi*100,0))+'% '+ticker for wi,ticker in zip(w,tickers)])


def gnaff_name_from_combination(c):
    return 'gnaaf_'+''.join([ str(cj) for cj in c]) + '.json'


GNAAF_NAMES = [gnaff_name_from_combination(c) for c in FAANG_COMBINATIONS]
GNAAF_WEIGHTS = [ portfolio_from_combination(c) for c in FAANG_COMBINATIONS]
GNAAF_LISTING = dict([(readable_portfolio_from_combination(c, tickers=FAANG_TICKERS), 'https://www.microprediction.org/stream_dashboard.html?stream=' + gnaff_name_from_combination(c).replace('.json', '')) for c in FAANG_COMBINATIONS])

NAAFG_METHODS = [('info', 1),  # The second entry is an exponent
                 ('info', 2),
                 ('info', 4),
                 ('kurtosis', 1),
                 ('kurtosis', 2),
                 ('kurtosis', 4),
                 ('semi', 1),
                 ('semi', 2),
                 ('semi', 4),
                 ('slope',1),
                 ('slope',2),
                 ('slope',4)]
NAAFG_NAMES = ['naafg_' + str(k) + '.json' for k, _ in enumerate(NAAFG_METHODS)] # Community portfolios




def create_listing_file():
    """
       Updates the stream listing
    """
    from microprediction.whereami import ROOT
    fn = os.path.join(ROOT, 'stream_examples_faang', 'stream_list.json')
    with open(fn,'wt') as fh:
        json.dump(GNAAF_LISTING,fh)


def scaled_portfolio_return(changes, w:[float]):
    """
       Compute scaled portfolio log changes from scaled asset log changes
    """
    w = np.array(w)/np.sum(w)   # Ensure weights normalized
    f = np.exp( np.array(changes)/1000.)  # Multiplicative increase in wealth
    w_post = float( np.inner( w, f) )    # Posterior unit portfolio wealth
    portfolio_change = 1000*math.log( w_post )
    return portfolio_change


def trim_and_chop(predictions):
    trimmed = [v if abs(v) < 100. else 100 * v / abs(v) for v in predictions]
    n_chop = int(math.ceil(len(trimmed)) / 50)
    chopped = trimmed[n_chop:-n_chop]
    return trimmed, chopped


def get_gnaff_prediction_metrics(write_key):
    """
       Get metrics for current predictions for GNAAF streams
       (Only the stream owner can do this)
    """
    the_means = list()
    the_stds = list()
    the_semis = list()
    the_kurtosis = list()
    the_slopes = list()
    reader = MicroReader()
    for name in GNAAF_NAMES:
        try:
            all_predictions = reader.get_predictions(name=name, write_key=write_key, delay=reader.DELAYS[2], strip=True, consolidate=True)
            _, chopped = trim_and_chop(all_predictions)
            neg_chopped = [ 0 if (ch>=0) else ch*ch for ch in chopped ]
            the_means.append(np.mean(chopped))
            the_stds.append(np.std(chopped))
            the_semis.append(math.sqrt(np.mean(neg_chopped)))
            the_kurtosis.append(kurtosis(chopped))
            # Vol horizon ratio
            all_predictions_long = reader.get_predictions(name=name, write_key=write_key, delay=reader.DELAYS[3], strip=True, consolidate=True)
            long_trimmed, long_chopped = trim_and_chop(all_predictions_long)
            slope = np.std(long_chopped)/(np.std(chopped))
            the_slopes.append(slope)
        except Exception as e:
            print('Something wrong with get_gnaff_prediction_metrics')
            print(e)
            the_means.append(0)
            the_stds.append(1)
            the_kurtosis.append(-0.01)
            the_semis.append(1)
            the_slopes.append(1)
    assert len(the_means)+len(the_stds)==2*len(GNAAF_NAMES)
    return the_means, the_stds, the_semis, the_kurtosis, the_slopes


def naafg_community_portfolios(write_key)->[[float]]:
    """
        A collection of community constructed portfolios of FAANG stocks
           write_key: the private key for LEGLESS_OCELOT, creator of the GNAAF portfolio return streams
    """
    the_means, the_stds, the_semis, the_kurtosis, the_slopes = get_gnaff_prediction_metrics(write_key=write_key)
    scaled_infos = [ 5*mn/st for mn, st in zip(the_means, the_stds)]
    the_translated_semis = [ s-min(the_semis)+1 for s in the_semis]
    the_scaled_semis = [ math.sqrt(s) for s in the_translated_semis]
    scaled_semi_infos = [ 1/ss for mn,ss in zip(the_means, the_scaled_semis)]
    scaled_kurtosis = [ 0.7*kt for kt in the_kurtosis]
    scaled_slopes = [ sl for sl in the_slopes ]
    the_portfolios = list()
    metrics = {'info':scaled_infos,'semi':scaled_semi_infos,
               'kurtosis':scaled_kurtosis,'slope':scaled_slopes}
    for metric_name,expon in NAAFG_METHODS:
        try:
            the_weighting = [ math.exp(expon*mtc) for mtc in metrics[metric_name] ]
        except OverflowError as e:
            print('Warning. Metric ' + str(metric_name) + ' yields an overflow ')
            n_port = len(metrics[metric_name])
            the_weighting = [ 1.0/n_port for _ in range(n_port)]


        the_unnormalized_portfolio = np.array([ 0 for _ in FAANG_NAMES ])
        for weight, w in zip( the_weighting, GNAAF_WEIGHTS):
            the_unnormalized_portfolio = the_unnormalized_portfolio + weight*np.array(w)
        the_portfolio = list( the_unnormalized_portfolio/sum(the_unnormalized_portfolio) )
        the_portfolios.append(the_portfolio)
    return the_portfolios


if __name__=='__main__':
    create_listing_file()
    from microprediction.config_private import LEGLESS_OCELOT
    ports = naafg_community_portfolios(write_key=LEGLESS_OCELOT)
    from pprint import pprint
    pprint(ports)

