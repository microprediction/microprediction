from credentials import EMYD_MAMMAL
from microprediction.streamskater import StreamSkater

# Example of a "skater" that uses the TimeMachines package for point estimates
# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com

try:
    from timemachines.skaters.simple.thinking import thinking_slow_and_fast
except ImportError:
    print('pip install timemachines')

if __name__=='__main__':
    skater = StreamSkater(write_key=EMYD_MAMMAL, f=thinking_slow_and_fast, use_std=True, max_active=1000)
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/emyd_mammal.py')
    skater.set_email('skater@gmail.com') # Only used to send redemption codes when you win daily prize
    skater.run()
