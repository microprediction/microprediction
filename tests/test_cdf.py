from microprediction.reader import MicroReader
mr = MicroReader(base_url='https://devapi.microprediction.org')

BASE_URLS=['https://api.microprediction.org','https://devapi.microprediction.org']

def test_get_cdf():
    for base_url in BASE_URLS:
        mr = MicroReader(base_url=base_url)
        res = mr.get_cdf_lagged(name='cop.json',delay=mr.DELAYS[1],num=15)
        assert len(res['x'])>3

def test_die_pdf():
    pdf = mr.get_discrete_pdf_lagged( name='die.json', delay=mr.DELAYS[1] )
    pass

def test_die_cdf():
    pdf = mr.get_discrete_pdf_lagged( name='die.json', delay=mr.DELAYS[1] )
    pass