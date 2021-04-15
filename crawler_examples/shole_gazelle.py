from microprediction.config_private import SHOLE_GAZELLE
from microprediction.streamskater import StreamSkater

# Example of a "skater" that uses the timemachines package for point estimates


try:
    from timemachines.skaters.simple import thinking_slow_and_fast
    using_tm = True
except ImportError:
    using_tm = False
    thinking_slow_and_fast = None


if __name__=='__main__':
    if using_tm:
        skater = StreamSkater(write_key=SHOLE_GAZELLE,f=thinking_slow_and_fast,use_std=False)
        skater.set_repository('https://github.com/microprediction/microprediction/blob/master/crawler_examples/shole_gazelle.py')
        skater.run()
    else:
        print('pip install timemachines')