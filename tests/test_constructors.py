from microprediction import MicroReader, MicroWriter, MicroCrawler, MicroConventions
from microprediction.conventions import create_key


def test_delays():
    mc = MicroConventions()
    assert len(mc.DELAYS)==4

def test_delays_1():
    mc = MicroReader()
    assert len(mc.DELAYS)==4

def test_delays_2():
    mc = MicroWriter(write_key=create_key(difficulty=7))
    assert len(mc.DELAYS)==4

def test_delays_3():
    mc = MicroCrawler(write_key=create_key(difficulty=7))
    assert len(mc.DELAYS)==4