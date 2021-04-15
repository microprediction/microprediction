from microprediction.config_private import SHOLE_GAZELLE
from microprediction.streamskater import StreamSkater

# Example of a "skater"


def wrap(x):
    """ Ensure x is a list of float """
    if x is None:
        return None
    elif isinstance(x,(float,int)):
        return [float(x)]
    else:
        return list(x)


def moving_avg_skater(y, s, k, a=None, t=None, e=None):
    """ Exponential moving average skater

           y : most recent observation
           s : skater state
           a : reserved for varibles known in advance
           t : observation time

        See https://github.com/microprediction/timemachines/blob/main/README.md
    """
    # This has a flat term structure of predictions and may not be sensible, but
    # you can find plenty of skaters in the timemachines package
    r = 0.1
    y0 = wrap(y)[0]   # Skaters take scaler or vector
    if not s.get('rho'):
        s = {'x':y0,
             'rho':r}
        assert 0 <= s['rho'] <= 1, 'Expecting rho=r to be between 0 and 1'
    else:
        assert abs(r-s['rho'])<1e-6,'rho=r is immutable'

    if y0 is None:
        return None, s, None
    else:
        s['x'] = s['rho']*s['x'] + (1-s['rho'])*y0         # Make me better !
        return [s['x']]*k, [1.0]*k, s


if __name__=='__main__':
    skater = StreamSkater(write_key=SHOLE_GAZELLE,f=moving_avg_skater,use_std=False)
    skater.set_repository('https://github.com/microprediction/microprediction/blob/master/crawler_examples/shole_gazelle.py')
    skater.run()