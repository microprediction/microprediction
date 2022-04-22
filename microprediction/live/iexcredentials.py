

def get_iex_key():
    try:
        from microprediction.config_private import IEX_KEY
        return IEX_KEY
    except ImportError:
        try:
            from credentials import IEX_KEY
            return IEX_KEY
        except ImportError:
            raise EnvironmentError('The IEX KEY needs to be supplied somehow')


if __name__=='__main__':
    print(get_iex_key())