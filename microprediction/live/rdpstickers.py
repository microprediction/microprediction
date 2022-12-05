RDPS_DESCRIPTIONS = {'e':'energy',
         'c':'communication',
         'y':'discretionary',
         'p':'discretionary',
         'f':'financials',
         'v':'health',
         'i':'industrials',
         'b':'materials',
         're':'real estate',
         'k':'technology',
         'u':'utilities'}


RDPS_TICKERS = ['xl'+suffix for suffix in RDPS_DESCRIPTIONS.keys() ]

RDPS_GENERIC_NAMES = [ 'rdps_' + ticker + '.json' for ticker in RDPS_TICKERS ]


if __name__=='__main__':
    print(RDPS_GENERIC_NAMES)