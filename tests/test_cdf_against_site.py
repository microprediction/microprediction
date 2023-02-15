from microprediction.reader import MicroReader
from microprediction.set_config import MICRO_TEST_CONFIG

BASE_URLS = MICRO_TEST_CONFIG['BASE_URLS'][:2]

# CDF is deprecated

def dont_test_get_cdf_die():
    for base_url in BASE_URLS:
        mr = MicroReader(base_url=base_url)
        res = mr.get_cdf_lagged(name='die.json', delay=mr.DELAYS[0], num=15)
        if not len(res['x']) > 3:
            assert False


def dont_test_die_pdf():
    for base_url in BASE_URLS:
        mr = MicroReader(base_url=base_url)
        pdf = mr.get_discrete_pdf_lagged(name='die.json', delay=mr.DELAYS[0])


def dont_test_troublesome():
    mr = MicroReader()
    pdf = mr.get_discrete_pdf_lagged(name='die.json', delay=mr.DELAYS[0])


def test_die_cdf():
    for base_url in BASE_URLS:
        mr = MicroReader(base_url=base_url)
        pdf = mr.get_discrete_pdf_lagged(name='die.json', delay=mr.DELAYS[0])


if __name__=='__main__':
    dont_test_die_cdf()
