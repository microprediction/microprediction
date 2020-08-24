from microprediction import SequentialStreamCrawler, SkewDist

try:
    from microprediction.config_private import SMEECH_CLAM
except ImportError:
    raise Exception('You need to create a write key')
import time


def include_crypto(name):
    """ Tell it to only look at some crypto streams """
    return 'btc' in name or 'c5_' in name

RESET_PERFORMANCE_ON_RESTART = True

if __name__ == '__main__':
    crawler = SequentialStreamCrawler(write_key=SMEECH_CLAM, machine_type=SkewDist, max_active=50, stop_loss=5)
    crawler.include_stream = include_crypto
    crawler.delete_performance()

    if RESET_PERFORMANCE_ON_RESTART:
        try:
            crawler.cancel_all()
        except Exception:
            print('Looks like you are using an older version than 0.11.13')
            for horizon in crawler.get_active():
                name, delay = crawler.split_horizon_name(horizon)
                crawler.cancel(name=name, delays=[delay])
                time.sleep(0.5)

    crawler.run()
