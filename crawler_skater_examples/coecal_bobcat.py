try:
    from timemachines.skaters.simple.thinking import thinking_precision_ensemble as f
except ImportError:
    print('pip install --upgrade pip')
    print('pip install timemachines')
    raise ValueError

try:
    from microprediction.config_private import COECAL_BOBCAT as WRITE_KEY
except ImportError:
    WRITE_KEY=None

from microprediction.streamskater import RegularFaangStreamSkater

if __name__=='__main__':
    skater = RegularFaangStreamSkater(write_key=WRITE_KEY, f=f, use_std=True, max_active=1000)
    skater.set_email('pcotton@intechinvestments.com')
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/cobega_bobcat.py')
    skater.run()
