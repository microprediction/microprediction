import ring, uuid, time

def mine():
    """ Infinite loop that prints keys """
    key_generator = MemorableUniqueIdentifier.key_generator(min_len=8, timeout=10000000000, verbose=True)
    for key in key_generator:
        print(key,flush=True)

memorable = MemorableUniqueIdentifier()

def muid4():
    return memorable.uuid4()


class MemorableUniqueIdentifier(object):
    # The hash of any unique identifier is somewhat human readable
    #
    #     key  = CuteUniqueIdentifier.uuid(min_len=7)         # Just like uuid, only really slow :) 
    #     code = CuteUniqueIdentifier.hash(key)               # Somewhat readable (stare at it)  f01dab1e-ca70-aff3-123acb6a576a68 
    #  english = CuteUniqueIdentifier.to_henglish(s)          # More readable yet (see it now?)  foldable-cat0-aff3-l23acb6a576a68   
    # 
    # Codes can be made more readable if we take the time to look up substrings in the dictionary 
    #
    #   pretty = CuteUniqueIdentifier.pretty(english)         # e.g.  'Foldable Cat'

    @staticmethod
    def hash(key):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, key))

    @staticmethod
    def is_henglish(s):
        return all( c in 'ol234s6t89abcdef-' for c in s)

    @staticmethod
    def to_henglish(code):
        """ Henglish """
        return code.replace('0', 'o').replace('1', 'l').replace('5', 's').replace('7', 't')

    @staticmethod
    def from_henglish(word):
        """ Make english look like Hex """
        return word.replace('o', '0').replace('l', '1').replace('s', '5').replace('t','7')

    @staticmethod
    def longest_word(phrase):
        assert MemorableUniqueIdentifier.is_henglish(phrase), "Not Henglish. Use Henglish.to_henglish first "
        phrase_sans = phrase.replace('-', '')
        words_found = list()
        k = MemorableUniqueIdentifier.max_word_len()
        while not words_found and k>=MemorableUniqueIdentifier.min_word_len():
            if phrase_sans[:k] in MemorableUniqueIdentifier.words()[k]:
                return phrase_sans[:k]
            k = k-1

    @staticmethod
    def longest_phrase(phrase):
        assert MemorableUniqueIdentifier.is_henglish(phrase), "Not Henglish. Use Henglish.to_henglish first "
        phrase_sans = phrase.replace('-', '')
        k=MemorableUniqueIdentifier.max_phrase_len()
        pairs_found = list()
        while not pairs_found and k>=6:
            if phrase_sans in MemorableUniqueIdentifier.phrases_of_len(k):
                return phrase_sans
            k = k-1

    @staticmethod
    def longest_word_or_phrase(phrase):
        word_found   = MemorableUniqueIdentifier.longest_word(phrase) or ''
        phrase_found = MemorableUniqueIdentifier.longest_phrase(phrase) or ''
        return word_found if len(word_found)>len(phrase_found) else phrase_found

    @staticmethod
    def split(phrase):
        """ Break pair (or singleton) back into two words (or one) """
        assert MemorableUniqueIdentifier.is_henglish(phrase), "Not Henglish. Use Henglish.to_henglish first "
        phrase_sans = phrase.replace('-', '')
        if MemorableUniqueIdentifier.is_word(phrase_sans):
            return [ phrase_sans ]
        elif len(phrase_sans)>2*MemorableUniqueIdentifier.min_word_len() and (phrase_sans in MemorableUniqueIdentifier.phrases_of_len(len(phrase_sans))):
            k = len(phrase_sans)
            parts = []
            k_min = MemorableUniqueIdentifier.min_word_len()
            k1 = k_min
            while not parts and k1<=MemorableUniqueIdentifier.max_phrase_len():
                w1 = phrase_sans[:k1]
                if w1 in MemorableUniqueIdentifier.words()[k1]:
                    w2 = phrase_sans[k1:]
                    k2 = k-k1
                    if k2>=k_min and w2 in MemorableUniqueIdentifier.words()[k - k1]:
                        parts = [w1,w2]
                k1 = k1+1
            return parts
        else:
            return None # Cannot split ...

    @staticmethod
    def pretty( phrase, separator=' ',capitalize=False ):
        """ Return a pretty version of a phrase such as:
                Foldable Cat
        """
        parts = MemorableUniqueIdentifier.split(phrase)
        cap_parts = [ part[0].upper()+part[1:] for part in parts ] if capitalize else parts
        return separator.join(cap_parts)

    @staticmethod
    def uuid(min_len=7, timeout=60*15):
        gen = MemorableUniqueIdentifier.key_generator(min_len=min_len, timeout=timeout)
        for key in gen:
            return key

    @staticmethod
    def key_generator(min_len=7, timeout=5, verbose=False, ):
        """ Returns generator that spits out valid keys whose hashes are recognizable Henglish words or word pairs """
        start_time = time.time()
        while time.time()<start_time+timeout:
            key      = MemorableUniqueIdentifier.random_identifier()
            code     = MemorableUniqueIdentifier.hash(key)
            hcode    = MemorableUniqueIdentifier.to_henglish(code=code)
            solution = MemorableUniqueIdentifier.longest_word_or_phrase(hcode)
            if len(solution)>min_len:
                if verbose:
                    pretty = MemorableUniqueIdentifier.pretty(solution, separator=' ', capitalize=True)
                    yield {"length":len(hcode),"pretty":pretty,"key":key}
                else:
                    yield key

    @ring.lru()
    @staticmethod
    def max_word_len():
        return max(list(MemorableUniqueIdentifier.words().keys()))

    @ring.lru()
    @staticmethod
    def min_word_len():
        return min(list(MemorableUniqueIdentifier.words().keys()))

    @staticmethod
    def max_phrase_len():
        return 13

    @ring.lru()
    @staticmethod
    def words():
        return {3: MemorableUniqueIdentifier.words3(),
                4: MemorableUniqueIdentifier.words4(),
                5: MemorableUniqueIdentifier.words5(),
                6: MemorableUniqueIdentifier.words6(),
                7: MemorableUniqueIdentifier.words7(),
                8: MemorableUniqueIdentifier.words8(),
                9: MemorableUniqueIdentifier.words9(),
                10:MemorableUniqueIdentifier.words10(),
                11:MemorableUniqueIdentifier.words11(),
                12:MemorableUniqueIdentifier.words12()}

    @staticmethod
    def is_word(word):
        words = MemorableUniqueIdentifier.words()
        return (len(word) in words) and (word in words[len(word)])

    @ring.lru()
    @staticmethod
    def phrases():
        return dict([(k, MemorableUniqueIdentifier.phrases_of_len(k)) for k in range(7, 14)])

    @ring.lru()
    @staticmethod
    def phrases_of_len(k):
        if k<=MemorableUniqueIdentifier.max_phrase_len() and k>=6:
            words = MemorableUniqueIdentifier.words()
            phrases = list()
            for k1 in range(k):
                k2 = k-k1
                if k1>=3 and k2>=3:
                    w1 = words[k1]
                    w2 = words[k2]
                    ph = [ a + b for a in w1 for b in w2 ]
                elif k1>=7:
                    ph = words[k1]
                else:
                    ph = []
                phrases.extend(ph)
            return phrases
        else:
            return []

    @staticmethod
    def words12():
        return []

    @staticmethod
    def words11():
        return []

    @staticmethod
    def words10():
        return ['obsolesced', 'obsolesces', 'calabooses',
                'saddleless', 'assessable', 'offsaddles',
                'coalfields']  # TODO: Add t's

    @staticmethod
    def words9():
        return ['baldfaced', 'boldfaced', 'coalfaces', 'decodable',
                'accolades', 'caboodles', 'closeable', 'coalesced',
                'ecolabels', 'scaleable', 'calaboose', 'deadballs',
                'deadfalls', 'escaladed', 'looseleaf', 'baseloads',
                'adolases', 'cascabells', 'cascables', 'classless',
                'abscesses', 'bloodless', 'baseballs', 'deadballs',
                'discalced', 'sociables', 'disclosed', 'siblicide',
                'localised', 'silicosis']  # TODO: Add t's

    @staticmethod
    def words8():
        return ['albedoes', 'allseeds', 'beefalos', 'boldface', 'caboosed',
                'cadelles', 'calloses', 'closable', 'coalless', 'codeless',
                'debacles', 'declasse', 'descales', 'ecolabel', 'faceless',
                'fadeless', 'foldable', 'laceless', 'leadless', 'leafless',
                'lobeless', 'secalose', 'socalled', 'sofabeds', 'cladodes',
                'descaled', 'socalled', 'badassed', 'baseload', 'calloses',
                'caseload', 'colossal', 'debossed', 'declasse', 'escalade',
                'fadeless', 'foodless', 'laceless', 'leasable', 'lobeless',
                'saleable', 'scalades', 'scalados', 'sealable', 'seafoods',
                'secalose', 'aldolase', 'allseeds', 'leadless'] # TODO: Add t's

    @staticmethod
    def words7():
        return ['albedoe', 'beefalo', 'befools', 'debacle', 'beadles', 'beefalo',
                'caboodl', 'befleas', 'belaced', 'boodles', 'caboose', 'codable',
                'doolees', 'elodeas', 'solaced', 'sofabed', 'seafood', 'fadable',
                'abodes0', 'cabals0', 'f1eeced', 'feedab1', '1abe1ed', 'facaded',
                'defaced', 'daffed0', 'cabbed0', 'baff1ed', 'acceded', '2faced0',
                'faded00', 'beaded0', 'decaded', 'ebbed00', 'acceded', 'effaced',
                'ceded00', 'dada007', 'debac1e', 'decada1', '1eafed0', 'fab1ed00',
                'dabb1e0', 'cab1ed0', '1ead000', 'b1ade00', 'f1ea000', 'flee000',
                'beef000', 'babe000', 'ee10000', 'dad0000', 'deadfa11', 'fadab1e',
                '1ad1ed0', 'be1aced', 'class00', 'leadles', 'fleeced', 'decease',
                'sealed0', 'scales0', 'felled0', 'leafles', 'eased00', 'decaf00',
                'called0', 'sell000', 'self000'] # TODO: Add t's

    @staticmethod
    def words6():
        return ['deflea','felted','foaled','fooled','leafed','lofted','albedo',
                'beadle','belted','bolted','boodle','coaled','colead','cooled',
                'doable','locoed','tabled','talced','aflood','defeat','fatted',
                'feeted','footed','batted','betted','boated','booted','catted',
                'coated','cooeed','debate','detect','fettle','feotal','battle',
                'blotto','boetel','bolete','bottle','cattle','lobate','locate',
                'oblate','ocelot','tablet','talbot','tectal','bootee','coatee',
                'cottae','delate','doolee','dottel','dottle','elated','elodea',
                'letted','looted','lotted','toledo','tooled','teated']  # TODO add more

    @staticmethod
    def words5():
        return ['abbas','babas','babes','beads','beefs',
                'cafes','cecas','dadas','deeds','focal',
                'faces','fades','feebs','feeds','decaf',
                'faced','cleft','cable','focal','cable',
                'celeb','coble','facet','facto','delft',
                'flood','abled','acold','baled','bedel',
                'blade','bleed','blood','clade','coled',
                'decal','dobla','dolce','defat','fated',
                'feted','abode','acted','adbot','adobe',
                'adobo','aloft','aloof','bated','booed',
                'cadet','cooed','coted','fetal','fleet',
                'fleet','float','flota','loofa','octad',
                'abele','betel','blate','bleat','bloat',
                'botel','cleat','cloot','eclat','elect',
                'obole','octal','table','telco','ebola',
                'ecole','afoot','betta','cooee','cotta',
                'octet','taboo','tacet','tecta','bottle',
                'fetta','dealt','delta','dotal','lated',
                'looed','toled','ladoo','datto','toted',
                'elate','latte','lotta','lotte','lotto',
                'telae','total','teaed']  # TODO add more

    @staticmethod
    def words4():
        return ['abba', 'abbe', 'abed', 'aced', 'baba', 'babe', 'bade', 'baff', 'bead', 'beef',
                'caca', 'cade', 'cafe', 'caff', 'ceca', 'cede', 'dace', 'dada', 'daff', 'dead',
                'deed', 'face', 'fade', 'feeb', 'feed', 'deaf', 'calf', 'clef', 'cafe', 'flab',
                'coof', 'fact', 'baft', 'delf', 'fled', 'fold', 'bald', 'bled', 'bold', 'clad',
                'clod', 'cold', 'daft', 'deaf', 'deft', 'fade', 'fado', 'feed', 'feod', 'food',
                'abed', 'aced', 'alef', 'bade', 'bead', 'bode', 'cade', 'cede', 'coda', 'code',
                'coed', 'dace', 'debt', 'deco', 'feal', 'feel', 'felt', 'flat', 'flea', 'floe',
                'foal', 'fool', 'leaf', 'left', 'loaf', 'loof', 'able', 'alec', 'bale', 'belt',
                'blae', 'blat', 'blet', 'blot', 'bola', 'bole', 'bolo', 'bolt', 'calo', 'celt',
                'clot', 'coal', 'cola', 'cole', 'colt', 'cool', 'cool', 'lace', 'lobe', 'lobo',
                'loca', 'obol', 'talc', 'doco', 'ecad', 'fale', 'felo', 'fate', 'feat', 'feet',
                'feta', 'fete', 'foot', 'tolf', 'abet', 'bate', 'batt', 'beat', 'beet', 'beta',
                'boat', 'boot', 'bota', 'bott', 'cate', 'cete', 'coat', 'coot', 'coot', 'cote',
                'oboe', 'tace', 'taco', 'tact', 'toco', 'acto', 'bato', 'bete', 'boto', 'dale',
                'dolt', 'lade', 'dale', 'deal', 'dele', 'delt', 'dole', 'dolt', 'lade', 'lead',
                'lede', 'load', 'olde', 'told', 'date', 'dato', 'deet', 'doat', 'odea', 'teed',
                'toad', 'toad', 'toed', 'alee', 'aloe', 'alto', 'late', 'leet', 'loot', 'lota',
                'olea', 'oleo', 'teel', 'tela', 'tele', 'tool', 'aloo', 'lato', 'leat', 'todo',
                'otto', 'tate', 'teat', 'toea', 'toot', 'etat', 'tete', 'tete', 'toto', 'feeb',
                'dobe', 'beal', 'tolt', 'loto']

    @staticmethod
    def words3():
        return ['aba', 'ace', 'add', 'baa', 'bad', 'bed', 'bee', 'cab', 'cad', 'dee', 'def', 'ebb',
                'ebb', 'fab', 'fad', 'fed', 'fee', 'ado', 'alb', 'ale', 'all', 'bad', 'bal', 'doc',
                'doe', 'dol', 'eel', 'eld', 'elf', 'ell', 'fab', 'fad', 'foe', 'lad', 'lea', 'led',
                'loo', 'oaf', 'oba', 'oca', 'oda', 'ode', 'old', 'cat', 'fab', 'cob', 'def', 'fad',
                'bad', 'bed', 'bod', 'cad', 'cod', 'dab', 'deb', 'doc', 'elf', 'alb', 'bal', 'bal',
                'bel', 'col', 'lab', 'lac', 'lob', 'bol', 'dob', 'dof', 'flo', 'aft', 'eft', 'aft',
                'fat', 'oof', 'act', 'bat', 'bee', 'boa', 'bot', 'cat', 'cee', 'cot' ,'eco', 'old',
                'lad', 'dot', 'eel', 'ale', 'eel', 'loo', 'eta', 'oat', 'oot', 'tae', 'tea', 'tee',
                'tet', 'toe', 'tot']

