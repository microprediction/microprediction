from microprediction.client import MicroClient, MicroReadClient
from contexttimer import Timer

def test_client():
    with Timer() as t:
        mc = MicroClient()
    assert mc.to_mnemonic(write_key=mc.write_key) in mc.dictionary7()
    assert(t.elapsed < 60*20 )

def test_nmemonic():
    write_key = "159e524a-145c-4cca-b098-ee06ea29b9b0"
    assert MicroReadClient.to_mnemonic(write_key=write_key) == 'caboodl'
