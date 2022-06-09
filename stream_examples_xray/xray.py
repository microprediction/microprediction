try:
    from microprediction.config_private import HEBDOMAD_LEECH as WRITE_KEY
except ImportError:
    raise EnvironmentError('Need stream write key')
from microprediction.polling import MultiChangePoll
from microprediction.live.xraytickers import get_xray_tickers
from microprediction.live.xrayprices import get_xray_prices
from microprediction.live.faang import scaled_portfolio_return
from microprediction.live.xrayportfolios import get_xray_portfolios, XRAY_PORTFOLIO_NAMES

# Minimalist example of publishing changes in a live quantity using MultiChangePoll

XRAY_PORTFOLIOS = get_xray_portfolios()
XRAY_TICKERS = get_xray_tickers()
XRAY_STOCK_NAMES = [ 'yarx_'+ticker+'.json' for ticker in XRAY_TICKERS ]
XRAY_NAMES = XRAY_STOCK_NAMES + XRAY_PORTFOLIO_NAMES


def func()->[float]:
    """
       The data retrieval function
    """
    return get_xray_prices()


def change_func(changes:[float])->[float]:
    """
        Function taking a vector of changes and returning a concatenation of
        the same changes and the portfolio returns
    """
    portfolio_changes = [scaled_portfolio_return(changes,w) for w in XRAY_PORTFOLIOS]
    return list(changes) + portfolio_changes


if __name__=='__main__':
    mcp = MultiChangePoll(write_key=WRITE_KEY, names = XRAY_NAMES, interval=5, func=func, change_func=change_func, with_copulas=True, min_change_count=10)
    mcp.set_repository('https://github.com/microprediction/microprediction/tree/master/stream_examples_xray')
    mcp.run()

