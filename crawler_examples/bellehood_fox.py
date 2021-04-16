from microprediction.config_private import BELLEHOOD_FOX
from microprediction.streamskater import ChoosySkatingFox

# Example of a "skater" that uses the TimeMachines package for point estimates
# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com

try:
    from timemachines.skaters.simple.movingaverage import aggressive_ema_ensemble
except ImportError:
    print('pip install timemachines')

if __name__=='__main__':
    skater = ChoosySkatingFox(write_key=BELLEHOOD_FOX, f=aggressive_ema_ensemble, use_std=False)
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_examples/bellehood_fox.py')
    skater.run()
