# Example of a "skater" that uses the TimeMachines package for point estimates
# See also https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/a_skater_template.py

from microprediction.streamskater import SkatingFox

# 1. Supply your WRITE_KEY
# You will have to create a credentials file, or otherwise modify this
# See https://microprediction.github.io/microprediction/writekeys.html

try:
    from credentials import HEALTHY_EEL as WRITE_KEY
except:
    try:
        from microprediction.private_config import HEALTHY_EEL as WRITE_KEY
    except:
        print('You need a write key. See https://microprediction.github.io/microprediction/writekeys.html', flush=True)
        raise NotImplementedError('You need to supply a write key')

# 2. Load a skater from the timemachines package
# See https://microprediction.github.io/timemachines/
try:
    from timemachines.skaters.simple.thinking import thinking_slow_and_slow as f
except ImportError:
    print('pip install timemachines')

# 3. Subclass some variety of StreamSkater and tell it where to go
# See https://github.com/microprediction/microprediction/blob/master/microprediction/streamskater.py for
# some choices of classes to derive from. Here we choose "SkatingFox" which comes with a default
# method fo specifying the spray of guesses around a point estimate provided by a timemachines point forecaster.
# This step is optional, as you can also just use StreamSkater or subclasses of the same directly. See
# the docs https://microprediction.github.io/microprediction/predict-using-python-microcrawler.html for
# more advice on how to modify a crawler.


class CompetitiveSkatingFox(SkatingFox):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def include_stream(self, name=None, **ignore):
        return ('~' not in name) and (
                    ('faang' in name) or ('sateb_' in name) or ('gnaaf' in name) or ('c2' in name) or (
                        'c5' in name) or ('fathom' in name) or ('xray' in name) or ('yarx' in name) or (
                                'electricity' in name))

    def include_delay(self, delay=None, name=None, **ignore):
        return delay >= self.delays[2]


# 4. Instantiate and run the crawler.
# If this script ever errors out, the crawler can recover somewhat gracefully.
# See https://www.microprediction.com/bouncing

if __name__ == '__main__':
    skater = CompetitiveSkatingFox(write_key=WRITE_KEY, f=f, use_std=False, max_active=1000)
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/healthy_eel.py')
    skater.run()
