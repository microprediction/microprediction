try:
    from microprediction.streamskater import StreamSkater
    from timemachines.skaters.tsa.tsaensembles import tsa_precision_combined_ensemble
except ImportError:
    print('pip install --upgrade pip')
    print('pip install timemachines')
    raise ValueError

try:
    from microprediction.config_private import FOELESS_STOAT as WRITE_KEY
except ImportError:
    WRITE_KEY=None

EMAIL_ID = "karthiks416@gmail.com"

class competitionsStreamSkater(StreamSkater):

    # This hits only those streams in competitions

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    
    def include_stream(self, name=None, **ignore):
        return ('~' not in name) and (('faang' in name) or ('gnaaf' in name) or ('c2' in name) or ('c5' in name)  or ('fathom' in name) or ('xray' in name) or ('yarx' in name) or ('electricity' in name))

    def include_delay(self, delay=None, name=None, **ignore):
        # We focus only on forecasting ~1hr delays 
        return delay>910


if __name__=='__main__':
    skater = competitionsStreamSkater(write_key=WRITE_KEY, f=tsa_precision_combined_ensemble, use_std=True, max_active=200)
    skater.set_email(EMAIL_ID)
    skater.run()