from microprediction.config_private import SCOTALE_BEE
from microprediction.streamskater import StreamSkater

# Example of a "skater" that uses the TimeMachines package for point estimates
# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com

try:
    from timemachines.skaters.simple.thinking import thinking_fast_and_slow
except ImportError:
    print('pip install timemachines')

if __name__=='__main__':
    skater = StreamSkater(write_key=SCOTALE_BEE, f=thinking_fast_and_slow, use_std=False, max_active=1000)
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/scotale_bee.py')
    skater.set_email("no_email@supplied.com")  # Only used to send you a voucher if you win a daily prize
    skater.run()
