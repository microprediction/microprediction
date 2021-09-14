from microprediction.config_private import DATABLE_LLAMA
from microprediction.streamskater import StreamSkater

# Example of a "skater" that uses the TimeMachines package for point estimates
# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com

try:
    from timemachines.skaters.simple.movingaverage import precision_ema_ensemble
except ImportError:
    print('pip install timemachines')

if __name__=='__main__':
    skater = StreamSkater(write_key=DATABLE_LLAMA, f=precision_ema_ensemble, use_std=True, max_active=1000)
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_examples/datable_llama.py')
    skater.run()
