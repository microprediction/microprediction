try:
  from microprediction.config_private import FATHOM_GAZELLE
except ImportError:
  raise('This example is not intended to be run. Obtain your own write_key https://www.microprediction.com/private-keys ')

from microprediction.polling import MultiChangePoll
from pprint import pprint
from microprediction import MicroWriter
import numpy as np
import math

# Produces conditional realized variance
# Produced conditional returns

COINS = 'bitcoin,ethereum'
C2_NAMES = [ 'c2_'+name+'.json' for name in COINS.split(',') ]

mw = MicroWriter(write_key=FATHOM_GAZELLE)

WEIGHTS = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]

#### Portfolio returns

def portfolio_names():
    return ['portfolio_c2_'+str(W)+'.json' for W in WEIGHTS ]

def portfolio_func(changes):
    values = list()
    for W in WEIGHTS:
        w0 = W/100.
        w1 = 1.0-w0
        change = 1000.*math.log( w0*math.exp(changes[0]/1000.) + w1*math.exp(changes[1]/1000.) )
        values.append(change)
    return values

# Quadratic variation in log(prices)

def quadratic_func(changes):
    dx = np.array([ changes ] )
    dxx = np.matmul(np.transpose(dx),dx)
    print(dxx)
    n_dim = len(C2_NAMES)
    values = list()
    for i in range(n_dim):
        for j in range(i,n_dim):
            values.append(dxx[i,j])
    return values

def quadratic_names():
    short_names = COINS.split(',')
    names = list()
    n_dim = len(C2_NAMES)
    for i in range(n_dim):
        for j in range(i,n_dim):
            names.append( 'quadratic_c2_'+short_names[i]+'_'+short_names[j]+'.json' )
    return names

# Predictions
def get_mean_quadratic_predictions():
    values = list()
    for name in quadratic_names():
        all_predictions = mw.get_own_predictions(name=name, delay=mw.DELAYS[2],strip=True, consolidate=True )
        trimmed_values = [ v if abs(v)<100. else 100*v/abs(v) for v in all_predictions]
        n_chop = int(math.ceil(len(trimmed_values))/20)
        values.append( np.mean(trimmed_values[n_chop:-n_chop]) )
    return values


def get_mean_portfolio_predictions():
    the_means = list()
    the_stds = list()
    for name in portfolio_names():
        all_predictions = mw.get_own_predictions(name=name, delay=mw.DELAYS[2], strip=True, consolidate=True)
        trimmed_values = [v if abs(v) < 100. else 100 * v / abs(v) for v in all_predictions]
        n_chop = int(math.ceil(len(trimmed_values)) / 50)
        chopped = trimmed_values[n_chop:-n_chop]

        the_means.append(np.mean(chopped))
        the_stds.append(np.std(chopped))
    return the_means, the_stds


def change_func(changes):
    """ Pre-pends the normalized changes and predictions """
    n_quad = len(quadratic_names())
    quadratic_changes = changes[:n_quad]
    portfolio_changes = changes[n_quad:]
    mean_q = get_mean_quadratic_predictions()
    mean_p, std_p = get_mean_portfolio_predictions()
    rel_q = [ qc/pqc for qc, pqc in zip(quadratic_changes,mean_q) ]
    rel_p = [ numer/denom for numer, denom in zip(portfolio_changes,std_p)]
    info_p = [ numer/denom for numer, denom in zip(mean_p,std_p)]
    # Compute weighted portfolio
    max_info = max(info_p)
    good_w = [ (math.exp(-abs(i_-max_info)),w) for w,i_ in zip(WEIGHTS,info_p) if i_>max_info-0.2 ]
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
    w_best_change = lw*portfolio_changes[low_per_index] + hw*portfolio_changes[high_per_index]
    w_best_diff  = [ w_best_change-pc for pc in portfolio_changes ]
    return [w_best_change, w_best, 100-w_best] + list(w_best_diff) + list(info_p) + list( mean_p) + list(std_p) + list( rel_p) + list(mean_q) + list( rel_q ) + list(changes)


def all_names():
    qn = quadratic_names()
    relative_quadratic = [ nm.replace('.json','_rel.json') for nm in qn ]
    mean_quadratic = [ nm.replace('.json','_expected.json') for nm in qn ]
    pn = portfolio_names()
    mean_portfolio = [nm.replace('.json', '_expected.json') for nm in pn]
    std_portfolio = [nm.replace('.json', '_std.json') for nm in pn]
    info_portfolio = [nm.replace('.json','_info.json') for nm in pn]
    rel_portfolio = [nm.replace('.json', '_rel.json') for nm in pn]
    diff_portfolio = [nm.replace('.json','_diff.json') for nm in pn]
    return ['best_c2.json','percent_c2_bitcoin.json','percent_c2_ethereum.json'] + diff_portfolio + info_portfolio + mean_portfolio + std_portfolio + rel_portfolio + mean_quadratic + relative_quadratic + qn + pn

def func():
    """ Returns portfolio returns """
    lagged_values = [ mw.get_lagged_values(name=name)[:2] for name in C2_NAMES ]
    print(lagged_values)
    if len(lagged_values[0])>=2:
        changes = [ lv[0]-lv[1] for lv in lagged_values ]
        return list( quadratic_func(changes) ) + list( portfolio_func(changes) )


if __name__=="__main__":
    # This part is just to tell people where the code that produces the stream is, for transparency
    from microprediction import MicroWriter
    MicroWriter(write_key=FATHOM_GAZELLE).set_repository('https://github.com/microprediction/microprediction/blob/master/stream_examples_crypto')

    print('testing',flush=True)
    names = all_names()
    values = func()
    augmented = change_func(values)
    assert len(augmented)==len(names)
    pprint(list(zip(names,augmented)))
    print('starting',flush=True)
    poll = MultiChangePoll(write_key=FATHOM_GAZELLE,func=func,names=names,interval=5,with_copulas=False, verbose=True, change_func=change_func)
    poll.run()