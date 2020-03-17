import uuid, re, sys, requests, muid

CONFIG  = requests.get('https://www.microprediction.com/config.json').json()
MIN_LEN = CONFIG['min_len']

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


class KeyConventions():

    @staticmethod
    def is_valid_key(key):
        """ Check if key is hash-memorable """
        return isinstance(key,str) and muid.validate(key)

    @staticmethod
    def create_key(difficulty=6):
        """ Create new write_key (string, not bytes) """
        return muid.create(difficulty=difficulty).decode()


class MicroConventions(NameConventions, ValueConventions, StatsConventions, KeyConventions):
    pass





