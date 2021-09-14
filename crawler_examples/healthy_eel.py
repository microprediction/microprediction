from microprediction.config_private import HEALTHY_EEL
from microprediction.streamskater import SkatingFox

# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com
# Example of a "skater" that uses the TimeMachines package for point estimates

try:
    from timemachines.skaters.simple.thinking import thinking_slow_and_slow
except ImportError:
    print('pip install timemachines')

if __name__=='__main__':
    skater = SkatingFox(write_key=HEALTHY_EEL, f=thinking_slow_and_slow, use_std=False, max_active=1000)
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_examples/healthy_eel.py')
    skater.run()
