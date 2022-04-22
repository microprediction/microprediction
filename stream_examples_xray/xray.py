from microprediction.config_private import HEBDOMAD_LEECH as WRITE_KEY
from microprediction.polling import MultiChangePoll
from microprediction.live.xraytickers import XRAY_NAMES, iex_scaled_log_xray
from microprediction.live.faang import scaled_portfolio_return
from microprediction.live.xrayportfolios import XRAY_PORTFOLIOS, XRAY_PORTFOLIO_NAMES

# Minimalist example of publishing changes in a live quantity using MultiChangePoll


def func()->[float]:
    """
       The data retrieval function
    """
    from microprediction.config_private import IEX_KEY  # <-- You'll need to modify this
    return iex_scaled_log_xray(api_key=IEX_KEY)


def change_func(changes:[float])->[float]:
    """
        Function taking a vector of changes and returning a concatenation of
        the same changes and the portfolio returns
    """
    portfolio_changes = [scaled_portfolio_return(changes,w) for w in XRAY_PORTFOLIOS]
    return list(changes) + portfolio_changes



if __name__=='__main__':
    mcp = MultiChangePoll(write_key=WRITE_KEY, names = XRAY_NAMES + XRAY_PORTFOLIO_NAMES, interval=45, func=func, with_copulas=True)
    mcp.set_repository('https://github.com/microprediction/microprediction/tree/master/stream_examples_xray')
    mcp.run()

