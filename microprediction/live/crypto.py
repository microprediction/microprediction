from pycoingecko import CoinGeckoAPI
from pprint import pprint


def names_and_prices():
    """ Returns bitcoin and ethereum in USD and EUR """
    # Just an example
    cg   = CoinGeckoAPI()
    data = cg.get_price(ids='bitcoin,ethereum', vs_currencies='usd,eur')
    # Flatten
    names  = list()
    prices = list()
    for coin, fx in data.items():
        for currency, price in fx.items():
            name  = coin+'_'+currency
            names.append(name)
            prices.append(price)

    return names, prices

if __name__=='__main__':
    names, values = names_and_prices()
    pprint(names)
    pprint(values)