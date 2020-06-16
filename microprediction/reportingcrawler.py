
# Only used for testing

from microprediction import MicroCrawler
import time, datetime, os
import numpy as np
from pprint import pprint

class ReportingCrawler(MicroCrawler):

        # Crawler created for testing purposes.
        # By all means use it for your own testing purposes by providing pass_callback and fail_callback

        def __init__(self, write_key, pass_callback, fail_callback):
            """
              :param pass_callback(dict)->bool  function that will be called if things look okay
              :param fail_callback(dict)->bool  function that will be called if things don't
            """
            super().__init__(stop_loss=2, min_lags=0, sleep_time=1, write_key=write_key, quietude=10, verbose=False)
            self.pass_callback = pass_callback
            self.fail_callback = fail_callback
            self.initial_balance = self.get_balance()

        def setup(self,**kwargs):
            """ Return error messages if any """
            pass

        def teardown(self,**kwargs):
            """ Return error messages if any """
            pass

        def candidate_streams(self,**ignore):
            """ Quickly quickly """
            return [name for name, sponsor in self.get_sponsors().items() if not '~' in name]

        def candidate_delays(self,**ignore):
            """ Fail fast """
            return [70]

        def sample(self, lagged_values, lagged_times=None, **ignore):
            if len(lagged_values or []) > 5:
                return super().sample(lagged_values=lagged_values, lagged_times=lagged_times)
            else:
                return sorted(
                    np.random.randn(self.num_predictions))

        def run_and_report(self, timeout=180, name='reporting_crawler'):
            """ Returns error report in form of dict """
            report = {'crawler': name, 'timeout': timeout, 'start_time': time.time(),
                      'start_datetime': str(datetime.datetime.now()),
                      'summary_page':'https://www.microprediction.org/home/'+self.write_key,
                      'base_url':self.base_url,
                      'virtual_env':os.getenv('VIRTUAL_ENV')}
            print(self.write_key)

            # Initial checks
            try:
                setup_errors = self.setup()
            except Exception as e:
                setup_errors = {'error':'error thrown by setup','message':str(e)}

            if setup_errors is None:
                # Run checks
                try:
                    self.run(timeout=timeout)
                    run_errors = None
                except Exception as e:
                    print(str(e), flush=True)
                    passed = False
                    run_errors = {'error':'run error','message':str(e)}
            else:
                run_errors = None

            if setup_errors is None and run_errors is None:
                # Teardown checks
                try:
                    teardown_errors = self.teardown()
                except Exception as e:
                    teardown_errors = {'error': 'error thrown by teardown', 'message': str(e)}
            else:
                teardown_errors = None

            any_errors = setup_errors or run_errors or teardown_errors
            if setup_errors:
                report.update(setup_errors)
            if run_errors:
                report.update(run_errors)
            if teardown_errors:
                report.update(teardown_errors)

            if not(any_errors) and self.pass_callback is not None:
                successfully_reported_pass = self.pass_callback(report)
                if successfully_reported_pass==False:
                    report.update({'reporting_failure':True})
                    self.fail_callback(report)
            if any_errors and (self.fail_callback is not None):
                self.fail_callback(report)
            pprint(report)


if __name__=="__main__":
    try:
        from microprediction.config_private import pass_callback, fail_callback, FLAMMABLE_COD
    except ImportError as e:
        pass_callback=None
        fail_callback=None

    crawler = ReportingCrawler(write_key=FLAMMABLE_COD, pass_callback=pass_callback, fail_callback=fail_callback)
    crawler.run_and_report(timeout=100, name='local test')
