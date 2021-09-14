from microprediction.config_private import SMEECH_CLAM
from microprediction.streamskater import StreamSkater

# Example of a "skater" that uses the TimeMachines package for point estimates
# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com

try:
    from timemachines.skaters.tsa.tsaconstant import tsa_p3_d0_q1
except ImportError:
    print('pip install timemachines')

if __name__=='__main__':
    skater = StreamSkater(write_key=SMEECH_CLAM, f=tsa_p3_d0_q1, use_std=False, max_active=1000)
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_examples/smeech_clam.py')
    skater.run()
