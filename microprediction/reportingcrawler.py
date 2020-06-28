
# Only used for testing

from microprediction import MicroCrawler
import time, datetime, os
import numpy as np
from pprint import pprint

class ReportingCrawler(MicroCrawler):

        # Crawler created for testing purposes.
        # By all means use it for your own testing purposes by providing pass_callback and fail_callback

        def __init__(self, write_key, pass_callback, fail_callback, **kwargs):
            """
              :param pass_callback(dict)->bool  function that will be called if things look okay
              :param fail_callback(dict)->bool  function that will be called if things don't
            """
            super().__init__(stop_loss=2, min_lags=0, sleep_time=1, write_key=write_key, quietude=10, verbose=False,**kwargs)
            self.pass_callback = pass_callback
            self.fail_callback = fail_callback
            self.initial_balance = self.get_balance()
            self.max_balance = self.initial_balance
            self.min_balance = self.initial_balance


        def setup(self,**kwargs):
            """ Return error messages if any """
            pass

        def downtime(self,seconds,**ignored):
            super().downtime(seconds=seconds,**ignored)
            self.min_balance = min(self.min_balance, self.get_balance())
            self.max_balance = max(self.max_balance, self.get_balance())

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

        def default_teardown_errors(self):
            """ Runs a list of ex-post tests """
            # Stale transactions?
            seconds_since_transaction = self.get_elapsed_since_transaction()
            if seconds_since_transaction is None:
                return {'error': 'inactivity', 'message': 'no transactions found'}
            if seconds_since_transaction > 1200:
                return {'error': 'inactivity', 'message': 'more than twenty mins since last transaction',
                        'seconds_since_transaction': seconds_since_transaction}
            # Stale confirms?
            seconds_since_confirm = self.get_elapsed_since_confirm()
            if seconds_since_confirm is None:
                return {'error':'inactivity','message':'no confirmations found'}
            if seconds_since_confirm>1200:
                return {'error':'inactivity','message':'more than twenty mins since last confirm','seconds_since_confirm':seconds_since_confirm}
            # Warn but don't error if balance is the same
            if abs(self.max_balance - self.min_balance) < 1e-5:
                pprint( {'warning': 'inactivity', 'warning message': 'min balance is same as max balance'} )
                print(' ',flush=True)


        def default_setup_errors(self):
            """ Run a bunch of very basic system checks """

            # Are APIs returning?
            try:
                # ... test nullary getters
                for method in ['get_confirms','get_sponsors','get_budgets','get_sponsors',
                               'get_balance','get_errors','get_overall','get_elapsed_since_transaction',
                               'get_elapsed_since_confirm','maybe_create_key','get_home']:
                    getattr(self,method)()

                # ... and a few requiring arguments
                method = 'get_leaderboard'
                self.get_leaderboard(name='cop.json')
                self.get_leaderboard(name='cop.json',delay=self.DELAYS[0])

                method = 'get_cdf'
                self.get_cdf(name='cop.json')
                self.get_cdf(name='three_body_x.json',delay=self.DELAYS[-1])

                method = 'get_lagged_times'
                self.get_lagged_times('cop.json')
                method = 'get_lagged_values'
                self.get_lagged_values('cop.json')

            except Exception as e:
                return {'error':'setup error','method':method,'message':str(e)}

        def run_and_report(self, timeout=180, name='reporting_crawler'):
            """ Returns error report in form of dict """
            report = {'crawler': name, 'timeout': timeout, 'start_time': time.time(),
                      'start_datetime': str(datetime.datetime.now()),
                      'summary_page':'https://api.microprediction.org/home/'+self.write_key,
                      'base_url':self.base_url,
                      'virtual_env':os.getenv('VIRTUAL_ENV')}
            print(self.write_key)
            pprint(report)

            # Initial checks
            setup_errors = self.default_setup_errors()
            if setup_errors is None:
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
                teardown_errors = self.default_teardown_errors()
                if teardown_errors is None:
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
        from microprediction.config_private import pass_callback, fail_callback, FLAMMABLE_COD, FLASHY_COYOTE
    except ImportError as e:
        pass_callback=None
        fail_callback=None

    crawler = ReportingCrawler(base_url='https://stableapi.microprediction.org',write_key=FLASHY_COYOTE, pass_callback=pass_callback, fail_callback=fail_callback)
    print(crawler.base_url)
    crawler.run_and_report(timeout=300, name='local test')
