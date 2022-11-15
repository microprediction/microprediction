# See also https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/a_skater_template.py

try:
    from timemachines.skaters.elo.eloensembles import elo_fastest_univariate_precision_ensemble as f
except ImportError:
    print('pip install --upgrade pip')
    print('pip install timemachines')
    raise ValueError

try:
    from microprediction.config_private import LEACHY_BOBCAT as WRITE_KEY
except ImportError:
    WRITE_KEY=None

from microprediction.streamskater import RegularFaangStreamSkater

if __name__=='__main__':
    skater = RegularFaangStreamSkater(write_key=WRITE_KEY, f=f, use_std=True, max_active=1000)
    skater.set_email('pcotton@intechinvestments.com')
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/leachy_bobcat.py')
    skater.run()
