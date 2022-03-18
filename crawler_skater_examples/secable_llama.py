try:
    from microprediction.config_private import SECABLE_LLAMA as WRITE_KEY
except ImportError:
    print('You need to supply a WRITE_KEY somehow')
    print('See https://www.microprediction.com/private-keys for explanation')

try:
    from timemachines.skaters.simple.movingaverage import precision_ema_ensemble
except ImportError:
    print('pip install --upgrade pip')
    print('pip install timemachines')


from microprediction.streamskater import RegularFaangStreamSkater

if __name__=='__main__':
    skater = RegularFaangStreamSkater(write_key=WRITE_KEY, f=precision_ema_ensemble, use_mean=False, use_std=True, max_active=1000)
    skater.set_repository(
        'https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/seccable_llama.py')
    skater.run()
