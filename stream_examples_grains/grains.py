from microprediction.config_private import ZOOBLAST_MOOSE as WRITE_KEY
from microprediction.polling import MultiChangePoll
from microprediction.live.grains import GRAIN_NAMES, iex_scaled_log_grains

# Minimalist example of publishing changes in a live quantity using MultiChangePoll


def func()->[float]:
    """
       The data retrieval function
    """
    from microprediction.config_private import IEX_KEY  # <-- You'll need to modify this
    return iex_scaled_log_grains(api_key=IEX_KEY)


if __name__=='__main__':
    mcp = MultiChangePoll(write_key=WRITE_KEY, names = GRAIN_NAMES, interval=5, func=func, with_copulas=True)
    mcp.set_repository('https://github.com/microprediction/microprediction/tree/master/stream_examples_grains')
    mcp.run()


