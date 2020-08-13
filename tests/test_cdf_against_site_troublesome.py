from microprediction.reader import MicroReader
from microprediction.set_config import MICRO_TEST_CONFIG

BASE_URLS = MICRO_TEST_CONFIG['BASE_URLS'][:2]


def test_troublesome_devapi():
    mr = MicroReader(base_url='https://devapi.microprediction.org')
    pdf = mr.get_discrete_pdf_lagged(name='die.json', delay=mr.DELAYS[1])

def test_troublesome_api():
    mr = MicroReader(base_url='https://api.microprediction.org')
    pdf = mr.get_discrete_pdf_lagged(name='die.json', delay=mr.DELAYS[1])

def test_troublesome_stableapi():
    mr = MicroReader(base_url='https://stableapi.microprediction.org')
    pdf = mr.get_discrete_pdf_lagged(name='die.json', delay=mr.DELAYS[1])