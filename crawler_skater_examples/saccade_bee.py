from microprediction.config_private import SACCADE_BEE
from microprediction.streamskater import SkatingFox

# Example of a "skater" that uses the TimeMachines package for point estimates
# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com
# See also https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/a_skater_template.py

try:
    from timemachines.skaters.simple.hypocraticensemble import slow_aggressive_ema_ensemble
except ImportError:
    print('pip install timemachines')

if __name__=='__main__':
    skater = SkatingFox(write_key=SACCADE_BEE, f=slow_aggressive_ema_ensemble, use_std=True, max_active=1000)
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/saccade_bee.py')
    skater.set_email("no_email@supplied.com")  # Only used to send you a voucher if you win a daily prize
    skater.run()
