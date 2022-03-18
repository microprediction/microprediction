from microprediction.config_private import LEGLESS_OCELOT as WRITE_KEY
from microprediction.polling import MultiChangePoll
from microprediction.live.faang import FAANG_TICKERS, N_FAANG, GNAAF_NAMES,\
    GNAAF_WEIGHTS, FAANG_NAMES, iex_scaled_log_faang, scaled_portfolio_return

# Illustrates the use of MultiChangePoll to publish changes to multiple live quantities, and
# also quantities derived from those changes. Here the func argument passed to MultiChangePoll
# specifies the live data whereas the change_func specifies how this will be transformed into a
# larger number of streams. Those streams include portfolio returns.

TICKERS = FAANG_TICKERS
N_TICKERS= N_FAANG
NAMES = FAANG_NAMES + GNAAF_NAMES    # FAANG streams are stock returns
                                     # GNAAF streams are portfolio returns


def func()->[float]:
    """
       The data retrieval function
    """
    from microprediction.config_private import IEX_KEY  # <-- You'll need to modify this
    return iex_scaled_log_faang(api_key=IEX_KEY)


def change_func(changes:[float])->[float]:
    """
        Function taking a vector of changes and returning a concatenation of
        the same changes and the portfolio returns
    """
    return list(changes) + [scaled_portfolio_return(changes,w) for w in GNAAF_WEIGHTS ]


if __name__=='__main__':
    mcp = MultiChangePoll(write_key=WRITE_KEY, names = NAMES, interval=10,
                          func=func, with_copulas=False, change_func=change_func)
    mcp.set_repository('https://github.com/microprediction/microprediction/tree/master/stream_examples_stocks')
    mcp.run()
