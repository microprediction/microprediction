from microprediction.config_private import SHOLE_GAZELLE
from microprediction.streamskater import StreamSkater

# Example of a "skater" that uses the TimeMachines package for point estimates

if __name__=='__main__':
    try:
        from timemachines.skaters.simple import thinking_slow_and_fast
        skater = StreamSkater(write_key=SHOLE_GAZELLE, f=thinking_slow_and_fast, use_std=False)
        skater.set_repository(
            'https://github.com/microprediction/microprediction/blob/master/crawler_examples/shole_gazelle.py')
        skater.run()
    except ImportError:
        print('pip install timemachines')