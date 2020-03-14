from microprediction.henglish import KeyConventions
from itertools import zip_longest

def test_generator():
    gen = KeyConventions.key_generator(min_len=3, timeout=2, verbose=True)
    for key in gen:
        print(key,flush=True)


def test_phrases():
    ph = KeyConventions.phrases_of_len(7)
    assert len(ph)>500

def test_split():
    q_and_a = {'foldablecat': ['foldable','cat'],
               "colossaleel": ['colossal','eel'],
               "obsolesced": ["obsolesced"],
               "aceeel": ['ace','eel']}
    for q, a in q_and_a.items():
        a1 = KeyConventions.split(q)
        assert all( a_==a1_ for a_,a1_ in zip_longest(a,a1) )

def test_is_henglish():
    q_and_a = {'localisa-ble98t3l4':False,
               'coalfields7':False,
               'obsolesced898tadsf':True,
               'albedoes-abba-ldeasdlf':True,
               'albedoes-abba-lkjasdlf':False,
               '8adkabba':False}
    for q,a in q_and_a.items():
        a1 = KeyConventions.is_henglish(q)
        assert a==a1

def test_longest_phrase():
    q_and_a = {'obsolesced898tadsf':'Obsolesced',
               'albedoes-abba-ldeasdlf':'Albedoes Abba',
               '8adabba':''}
    for q,a in q_and_a.items():
        ph = KeyConventions.longest_phrase(phrase=q)
        ph_pretty = KeyConventions.pretty(ph, separator=' ', capitalize=True)
        assert ph==a

