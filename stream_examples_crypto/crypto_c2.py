from microprediction.config_private import EMBLOSSOM_MOTH as WRITE_KEY  # Burn your own with new_key(difficulty=13)
from microprediction.polling import MultiChangePoll
from pycoingecko import CoinGeckoAPI
import math
from pprint import pprint
import numpy as np
import time

# This is the actual code used to generate the 'c2' series
# Everything is driven off changes in bitcoin and ethereum prices
from microprediction import MicroWriter


COINS = 'bitcoin,ethereum'
C2_NAMES = ['c2_change_in_log_' + name + '.json' for name in COINS.split(',')]
WEIGHTS = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]

mw = MicroWriter(write_key=WRITE_KEY)
mw.set_repository('https://github.com/microprediction/microprediction/tree/master/stream_examples_crypto')


def func():
    """ Returns five large cap coins in USD """
    cg   = CoinGeckoAPI()
    data = cg.get_price(ids=COINS, vs_currencies='usd')
    pprint(data)
    raw  = [ data[coin]['usd'] for coin in COINS.split(',') ]
    return [ 1000*math.log(v) for v in raw ]


def quadratic_moments(changes):
    up_changes = [ c if c>0 else 0.1*c for c in changes ]
    dn_changes = [ c if c<0 else 0.1*c for c in changes ]
    dx = np.array([ changes ] )
    dxu = np.array([ up_changes ] )
    dxl = np.array([ dn_changes ] )
    dxx = np.matmul(np.transpose(dx),dx)
    dxxu = np.matmul(np.transpose(dxu), dxu)
    dxxl = np.matmul(np.transpose(dxl), dxl)
    print(dxx)
    n_dim = len(C2_NAMES)
    values = list()
    for i in range(n_dim):
        for j in range(i,n_dim):
            values.append(dxx[i,j]) # full
            values.append(dxxl[i, j])  # lower
            values.append(dxxu[i, j])  # upper
    assert len(values)==len(quadratic_moments_names())
    return values


def quadratic_moments_names():
    short_names = COINS.split(',')
    typs = ['full','lower','upper']
    names = list()
    n_dim = len(C2_NAMES)
    for i in range(n_dim):
        for j in range(i,n_dim):
            for typ in typs:
                nm = 'c2_quadratic_' + typ + '_' + short_names[i]+'_'+short_names[j]+'.json'
                names.append( nm )
    return names




def get_portfolio_changes(changes):
    values = list()
    for W in WEIGHTS:
        w0 = W/100.
        w1 = 1.0-w0
        change = 1000.*math.log( w0*math.exp(changes[0]/1000.) + w1*math.exp(changes[1]/1000.) )
        values.append(change)
    assert len(values)==len(portfolio_changes_names())
    return values

def portfolio_changes_names():
    return ['c2_rebalanced_'+str(W)+'.json' for W in WEIGHTS ]



def get_mean_quadratic_predictions():
    values = list()
    for name in quadratic_moments_names():
        if 'lower' in name:
            try:
                all_predictions = mw.get_own_predictions(name=name, delay=mw.DELAYS[-2],strip=True, consolidate=True )
                trimmed_values = [ v if abs(v)<100. else 100*v/abs(v) for v in all_predictions]
                n_chop = int(math.ceil(len(trimmed_values))/20)
                values.append( np.mean(trimmed_values[n_chop:-n_chop]) )
            except:
                print('No predictions yet or wrong key?')
                values.append(0)
    return values


def quadratic_prediction_names():
    return [nm.replace('lower_','lower_mean_') for nm in quadratic_moments_names() if 'lower' in nm]



# Portfolios based on hypothetical portfolio predictions


def get_portfolio_predictions():
    the_means = list()
    the_stds = list()
    for name in portfolio_changes_names():
        try:
            all_predictions = mw.get_own_predictions(name=name, delay=mw.DELAYS[2], strip=True, consolidate=True)
            trimmed_values = [v if abs(v) < 100. else 100 * v / abs(v) for v in all_predictions]
            n_chop = int(math.ceil(len(trimmed_values)) / 50)
            chopped = trimmed_values[n_chop:-n_chop]
            the_means.append(np.mean(chopped))
            the_stds.append(np.std(chopped))
        except AttributeError:
            print('Um...')
            the_means.append(0)
            the_stds.append(1)
    assert len(the_means)+len(the_stds)==len(portfolio_prediction_names())
    return the_means, the_stds


def portfolio_prediction_names():
    mean_portfolio = [nm.replace('.json', '_mean.json') for nm in portfolio_changes_names()]
    std_portfolio = [nm.replace('.json', '_std.json') for nm in portfolio_changes_names()]
    return mean_portfolio + std_portfolio



def get_best_weights_from_portfolio_predictions(mean_p,std_p):
    """ Pre-pends the normalized changes and predictions """
    info_p = [ numer/denom for numer, denom in zip(mean_p,std_p)]
    max_info = max(info_p)
    good_w = [ (math.exp(-5.0*abs(i_-max_info)),w) for w,i_ in zip(WEIGHTS,info_p) if i_>max_info-0.1 ]
    good_w_sum = sum( [m_ for m_,w_ in good_w ])
    good_w_wsum = sum( [m_*w_ for m_,w_ in good_w])
    w_best = good_w_wsum/good_w_sum

    # Compute ratio of weighted portfolio returns to the fixed weight portfolios

    def _low_high(offset):
        """ Represent a float offset as combination of two discrete ones """
        l = math.floor(offset)
        u = math.ceil(offset)
        r = offset - l
        return (l, 1 - r), (u, r)

    (l,lw), (h, hw) = _low_high(w_best / 5.0)
    low_per = int(5*l)
    high_per = int(5*h)
    low_per_index = WEIGHTS.index(low_per)
    high_per_index = WEIGHTS.index(high_per)

    return low_per_index, lw, high_per_index, hw, w_best


def best_info_portfolio_changes(mean_p, std_p, portfolio_changes):
    low_per_index, lw, high_per_index, hw, w_best = get_best_weights_from_portfolio_predictions(mean_p=mean_p, std_p=std_p)
    w_best_change = lw * portfolio_changes[low_per_index] + hw * portfolio_changes[high_per_index]
    w_best_diff = [w_best_change - pc for pc in portfolio_changes]
    values = [w_best_change, w_best, 100 - w_best] + w_best_diff
    assert len(values)==len(best_info_portfolio_names())
    return values


def best_info_portfolio_names():
    diff_portfolio = [nm.replace('rebalanced', 'info_minus_rebalanced') for nm in portfolio_changes_names()]
    return ['c2_info_return.json', 'c2_info_percent_bitcoin.json', 'c2_info_percent_ethereum.json'] + diff_portfolio


# Combine what we need into a change_func that will be triggered at the same time

def change_func(changes):
    portfolio_changes = get_portfolio_changes(changes)
    mean_p, std_p = get_portfolio_predictions()
    best_changes = best_info_portfolio_changes(mean_p=mean_p, std_p=std_p, portfolio_changes=portfolio_changes)
    q_moments = list( quadratic_moments(changes) )
    return changes + q_moments + list(portfolio_changes) + list(get_mean_quadratic_predictions()) + list(best_changes) + list(mean_p) + list(std_p)


def change_names():
    return quadratic_moments_names() + portfolio_changes_names() + quadratic_prediction_names() + best_info_portfolio_names() + portfolio_prediction_names()


if __name__=="__main__":
    print('testing',flush=True)
    f1 = func()
    time.sleep(70)
    f2 = func()
    changes = [ f2i-f1i for f1i, f2i in zip(f1,f2) ]
    cf = change_func(changes)

    print('starting',flush=True)
    names = C2_NAMES + change_names()
    assert len(f1)==len(C2_NAMES)
    assert len(cf)==len(names)

    pprint(dict(zip(names, list(changes)+list(cf))))

    poll = MultiChangePoll(write_key=WRITE_KEY, func=func, names=names, interval=10, with_copulas=False, verbose=True, change_func=change_func)

    # Attribution

    poll.run()
