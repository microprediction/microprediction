from microprediction.config_private import SECABLE_LLAMA as WRITE_KEY
from microprediction.streamskater import StreamSkater

# Example of a "skater" that uses the TimeMachines package for point estimates
# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com

try:
    from timemachines.skaters.simple.movingaverage import precision_ema_ensemble as f
except ImportError:
    print('pip install timemachines')

if __name__=='__main__':
    skater = StreamSkater(write_key=WRITE_KEY, f=f, use_std=True, max_active=1000)
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/datable_llama.py')
    skater.set_email("pcotton@intechinvestments.com")  # Only used to send you a voucher if you win a daily prize
    skater.run()
