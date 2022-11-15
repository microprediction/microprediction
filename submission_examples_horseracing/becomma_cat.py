import time
try:
    from credentials import BECOMMA_CAT as WRITE_KEY
except:
    WRITE_KEY=None


# Step 2: Instantiate writer
from microprediction import MicroWriter
mw = MicroWriter(write_key=WRITE_KEY)
mw.set_repository('https://github.com/microprediction/microprediction/blob/master/submission_examples_horseracing/becomma_cat.py')

# These are the streams we'll try to predict
# Example: https://www.microprediction.org/stream_dashboard.html?stream=horse_finish_5
FINISH_NAMES = ['horse_finish_'+str(k)+'.json' for k in range(1,6)]

# And these provide a clue... they are the market prices to win
PRICE_NAMES  = ['horse_price_'+str(k)+'.json' for k in range(1,6)]


def horsing_around():
    # Step 3: Grab the prices of each horse
    dividends = [ float(mw.get_current_value(name)) for name in PRICE_NAMES]

    # Step 4: Somehow determine probabilities of finish positions, or otherwise provide 225 samples
    # Sub in your own method here.
    try:
        from winning.lattice_simulation import simulate_performances, longshot_adjusted_dividends, placegetters_from_performances
        from winning.lattice import skew_normal_density, densities_from_offsets
        from winning.lattice_calibration import dividend_implied_ability
    except ImportError:
        raise EnvironmentError('pip install --upgrade winning')
    unit = 0.01
    density = skew_normal_density(L=501, unit=0.01, scale=1.0, a=0.5)
    adj_dividends = longshot_adjusted_dividends(dividends=dividends,longshot_expon=1.04)
    offsets = dividend_implied_ability(dividends=adj_dividends, density=density)
    densities = densities_from_offsets(density=density, offsets=offsets)
    performances = simulate_performances(densities=densities, n_samples=225, add_noise=True, unit=unit)
    placegetters = placegetters_from_performances(performances=performances, n=5)

    # Step 5: Submit
    for finish_name, horse_placings in zip(FINISH_NAMES,placegetters):
        values = sorted([ f+1 for f in horse_placings ])
        for delay in mw.DELAYS:
            mw.submit(name=finish_name,values=values, delay=delay)


if __name__=='__main__':
    # This is intended to be run from cron once per hour.
    st = time.time()
    while time.time()-st<60*58:
        time.sleep(71)
        horsing_around()
