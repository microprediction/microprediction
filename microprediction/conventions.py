import uuid, re, sys, muid, requests, time
from muid.mining import mine_once
from getjson import getjson

def testing_url():
    return "https://devapi.microprediction.org"

def default_url():
    return "https://api.microprediction.org"

class KeyConventions():

    @staticmethod
    def is_valid_key(key):
        """ Check if key is hash-memorable """
        return isinstance(key,str) and muid.validate(key)

    @staticmethod
    def create_key(difficulty=6):
        """ Create new write_key (string, not bytes) """
        return muid.create(difficulty=difficulty).decode()

    @staticmethod
    def maybe_create_key(seconds=1,difficulty=12):
        """ Find a MUID, maybe
             difficulty:  int  minimum length of the memorable part of the hash
        """
        quota = 100000000
        count = 0
        start_time = time.time()
        dffclty = difficulty
        while time.time()-start_time<seconds:
            report, dffclty, count = mine_once(dffclty, count, quota)
            if report:
                return report[0]["key"]


new_key = KeyConventions.create_key

class NameConventions(object):

    @staticmethod
    def sep():
        return '::'

    @staticmethod
    def is_plain_name(name: str):
        return NameConventions.is_valid_name(name) and not "~" in name

    @staticmethod
    def is_valid_name(name: str):
        name_regex = re.compile(r'^[-a-zA-Z0-9_~.:]{1,200}\.[json,html]+$', re.IGNORECASE)
        return (re.match(name_regex, name) is not None) and (not NameConventions.sep() in name)

    @staticmethod
    def random_name():
        return str(uuid.uuid4()) + '.json'

    def horizon_name(self, name, delay):
        """ Convention is used for performance and other hashes """  # Move to MicroConventions
        return str(delay)+self.sep() + name

    def split_horizon_name(self, key):
        spl = key.split(self.sep())
        name = spl[1]
        delay = int(spl[0])
        return name, delay

class ValueConventions(object):

    @staticmethod
    def is_scalar_value(value):
        try:
            fv = float(value)
            return True
        except:
            return False

    @staticmethod
    def is_valid_value(value):
        return isinstance(value, (str, int, float)) and sys.getsizeof(value) < 100000

    @staticmethod
    def is_small_value(value):
        """ Used to determine how to store history for dict like values """
        return sys.getsizeof(value) < 1200


class StatsConventions():

    @staticmethod
    def percentile_abscissa():
        return [-8., -5., -4, -3, -2.5, -2.0, -1.5, -1.25, -1, -0.8, -0.6, -0.4, -0.2, -0.1, -0.05, -0.02, -0.01, 0.,
                0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1., 1.25, 1.5, 2.0, 2.5, 3., 4., 5., 8.]


class MicroConventions(NameConventions, ValueConventions, StatsConventions, KeyConventions):

    def __init__(self, base_url=None, num_predictions=None, min_len=None, min_balance=None, delays=None) :
        """ Establish connection and adopt configuration parameters from site, if not provided """
        self.base_url       = base_url or default_url()
        default_config      = getjson(url='https://config.microprediction.org/config.json',
                             failover_url='https://stableconfig.microprediction.org/config.json')
        self.delays          = delays or default_config["delays"]
        self.num_predictions = num_predictions or default_config["num_predictions"]
        self.min_len         = min_len or default_config["min_len"]
        self.min_balance     = min_balance or default_config["min_balance"]



