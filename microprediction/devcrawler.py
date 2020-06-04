
# Only used for testing

from microprediction import MicroCrawler
import time, datetime
import numpy as np
from pprint import pprint

class DevTestingCrawler(MicroCrawler):

        " Crawler used for testing code releases "

        def __init__(self, write_key, pass_callback, fail_callback):
            super().__init__(stop_loss=2, min_lags=0, sleep_time=1, write_key=write_key, quietude=10, verbose=False)
            self.pass_callback = pass_callback
            self.fail_callback = fail_callback

        def candidate_streams(self,**ignore):
            """ He'll try anything """
            return [name for name, sponsor in self.get_sponsors().items()]

        def candidate_delays(self,**ignore):
            """ Fail fast """
            return [70]

        def sample(self, lagged_values, lagged_times=None, **ignore):
            if len(lagged_values or []) > 5:
                return super().sample(lagged_values=lagged_values, lagged_times=lagged_times)
            else:
                return sorted(
                    np.random.randn(self.num_predictions))

        def run_dev_tests(self,timeout=180,name='devtest_crawler'):
            report = {'crawler': name, 'timeout': timeout, 'start_time': time.time(),
                      'start_datetime': str(datetime.datetime.now())}
            print(self.write_key)
            passed = True
            error  = None

            try:
                self.run(timeout=timeout)
            except Exception as e:
                print(str(e), flush=True)
                passed = False
                report.update({'error':error})

            if passed and self.pass_callback is not None:
                pass_reporting = self.pass_callback(report)
                if pass_reporting==False:
                    report.update({'reporting_failure':True})
                    self.fail_callback(report)
            if not(passed) and self.fail_callback is not None:
                self.fail_callback(report)
            pprint(report)


if __name__=="__main__":
    try:
        from microprediction.config_private import pass_callback, fail_callback, FLAMMABLE_COD
    except ImportError as e:
        pass_callback=None
        fail_callback=None

    crawler = DevTestingCrawler(write_key=FLAMMABLE_COD,pass_callback=pass_callback,fail_callback=fail_callback)
    crawler.run_dev_tests(timeout=10,name='local test')
