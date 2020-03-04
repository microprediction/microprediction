import uuid, re, sys

class MicroConventions(object):

    @staticmethod
    def strength():
        return 9

    @staticmethod
    def min_key_len():
        return 18

    @staticmethod
    def is_plain_name(name: str):
        return MicroConventions.is_valid_name(name) and not "~" in name

    @staticmethod
    def is_small_value(value):
        """ Somewhat arbitrary """
        return sys.getsizeof(value) < 1200

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
    def is_valid_name(name: str):
        name_regex = re.compile(r'^[-a-zA-Z0-9_~.:]{1,200}\.[json,html]+$', re.IGNORECASE)
        return (re.match(name_regex, name) is not None) and (not MicroConventions.sep() in name)

    @staticmethod
    def sep():
        return "::"

    @staticmethod
    def random_key():
        return str(uuid.uuid4())

    @staticmethod
    def is_valid_key(key):
        return isinstance(key, str) and len(key) > MicroConventions.min_key_len()

    @staticmethod
    def random_name():
        return MicroConventions.random_key() + '.json'

    @staticmethod
    def hash(key):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, key))

    @staticmethod
    def is_english_word(word,dictionary=None):
        dictionary = dictionary or MicroConventions.default_dictionary()
        return word in dictionary

    @staticmethod
    def default_dictionary():
        return MicroConventions.dictionary7() if MicroConventions.strength()==7 else MicroConventions.dictionary9()

    @staticmethod
    def is_vanity_key(write_key=None,write_code=None,dictionary=None):
        dictionary = dictionary or MicroConventions.default_dictionary()
        write_code = write_code or MicroConventions.hash(write_key)
        candidate_word = MicroConventions.to_mnemonic(write_code=write_code)
        return MicroConventions.is_english_word(candidate_word, dictionary=dictionary)

    @staticmethod
    def new_vanity_key_estimate():
        # Can take quite a long time :)
        return "up to ten minutes or so " if MicroConventions.strength()==7 else "all day."

    @staticmethod
    def new_vanity_key(dictionary=None):
        # Can take quite a long time :)
        remaining = int(1e9)
        dictionary = dictionary or MicroConventions.default_dictionary()
        while remaining:
            remaining = remaining - 1
            write_key = MicroConventions.random_key()
            if MicroConventions.is_vanity_key(write_key=write_key, dictionary=dictionary):
                return write_key
        raise Exception('Failed to generate vanity key')

    @staticmethod
    def to_mnemonic(write_key=None, write_code=None):
        write_code = write_code or MicroConventions.hash(write_key)
        return write_code[-12:].replace('1','l').replace('0','o').replace('5','s')

    @staticmethod
    def dictionary11():
        return ['localisable','disclosable','dissociable']

    @staticmethod
    def dictionary10():
        return ['obsolesced','obsolesces','calabooses',
                'saddleless','assessable','offsaddles',
                'coalfields','diabolical','labialised',
                'disclosals','diabolises','disclasses',
                'socialised']

    @staticmethod
    def dictionary9():
        return [ 'baldfaced','boldfaced','coalfaces','decodable',
                 'accolades','caboodles','closeable','coalesced',
                 'ecolabels','scaleable','calaboose','deadballs',
                 'deadfalls','escaladed','looseleaf','baseloads',
                 'adolases','cascabells','cascables','classless',
                 'abscesses','bloodless','baseballs','deadballs',
                 'discalced','sociables','disclosed','siblicide',
                 'localised','silicosis']

    @staticmethod
    def dictionary8():
        return ['albedoes','allseeds','beefalos','boldface','caboosed',
                'cadelles','calloses','closable','coalless','codeless',
                'debacles','declasse','descales','ecolabel','faceless',
                'fadeless','foldable','laceless','leadless','leafless',
                'lobeless','secalose','socalled','sofabeds','cladodes',
                'descaled','socalled','badassed','baseload','calloses',
                'caseload','colossal','debossed','declasse','escalade',
                'fadeless','foodless','laceless','leasable','lobeless',
                'saleable','scalades','scalados','sealable','seafoods',
                'secalose','aldolase','allseeds','leadless']

    @staticmethod
    def dictionary7():
        return [ 'albedoe','beefalo','befools','debacle','beadles','beefalo',
                 'caboodl','befleas','belaced','boodles','caboose','codable',
                 'doolees','elodeas','solaced','sofabed','seafood','fadable',
                 'abodes0','cabals0','f1eeced','feedab1','1abe1ed','facaded',
                 'defaced','daffed0','cabbed0','baff1ed','acceded','2faced0',
                 'faded00','beaded0','decaded','ebbed00','acceded','effaced',
                 'ceded00','dada007','debac1e','decada1','1eafed0','fab1ed00',
                 'dabb1e0','cab1ed0','1ead000','b1ade00','f1ea000','flee000',
                 'beef000','babe000','ee10000','dad0000','deadfa11','fadab1e',
                 '1ad1ed0','be1aced','class00','leadles','fleeced','decease',
                 'sealed0','scales0','felled0','leafles','eased00','decaf00',
                 'called0','sell000','self000']

    @staticmethod
    def percentile_abscissa():
        return [-8., -5., -4, -3, -2.5, -2.0, -1.5, -1.25, -1, -0.8, -0.6, -0.4, -0.2, -0.1, -0.05, -0.02, -0.01, 0.,
                0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1., 1.25, 1.5, 2.0, 2.5, 3., 4., 5., 8.]

    @staticmethod
    def random_title():
        return {"name": MicroConventions.random_name(), "write_key": MicroConventions.random_key()}