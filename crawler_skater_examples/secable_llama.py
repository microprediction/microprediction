from microprediction.config_private import SECABLE_LLAMA as WRITE_KEY
from microprediction.streamskater import SkatingFox

# Example of a "skater" that uses the TimeMachines package for point estimates
# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com
# See also https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/a_skater_template.py


try:
    from timemachines.skaters.simple.hypocraticensemble import slow_precision_ema_ensemble as f
except ImportError:
    print('pip install timemachines')
    raise EnvironmentError

if __name__=='__main__':
    skater = SkatingFox(write_key=WRITE_KEY, f=f, use_std=True, max_active=1000)
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/datable_llama.py')
    skater.set_email("pcotton@intechinvestments.com")  # Only used to send you a voucher if you win a daily prize
    skater.run()
