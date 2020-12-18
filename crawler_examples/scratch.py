
FLASHY_COYOTE='4e57ef0ca8a661496c40a2b2c0999de1'

from microprediction.reportingcrawler import ReportingCrawler
import requests, time, os, sys
from getjson import getjson
from pprint import pprint


def logger_url_root():
    env = os.getenv('VIRTUAL_ENV')
    if env and 'prod' in env:
        return 'http://prodtests.microprediction.org/'
    else:
        return 'http://devtests.microprediction.org/'

def pass_logger_url():
    return logger_url_root()+'crawler_pass_logger'

def fail_logger_url():
    return logger_url_root()+'crawler_fail_logger'

def prod_or_dev():
    env = os.getenv('VIRTUAL_ENV')
    return 'prod' if (not env or 'prod' in env) else 'dev'

def fail_email_url():
    url = 'http://alerts.microprediction.org/prodemail?text="Failing crawler: prod environ. Check http://prodtests.microprediction.org "'
    return url.replace('prod',prod_or_dev())

def fail_txt_url():
    url = 'http://alerts.microprediction.org/txt?body="See http://prodtests.microprediction.org/fails.json'
    return url.replace('prod',prod_or_dev())

def pass_callback(report):
    """ Should return True if successful """
    print('Reporting success',flush=True)
    report = report or dict()
    res = requests.post(url=pass_logger_url(), data=report)
    if res.status_code!=200:
        report.update({'message':'prodtest down','prodtest_status_code':res.status_code})
    else:
        pprint(report)
        print('Reported passing test to prodtests ',flush=True)
        return res.status_code == 200

def fail_callback(report):
    """ Should return True if successful """
    report.update({'virtual_env':os.getenv('VIRTUAL_ENV')})
    print('Reporting failure',flush=True)
    pprint(report)
    print('Sending email alerts',flush=True)
    res1 = requests.get(fail_email_url())
    print('Sending txt alerts',flush=True)
    res2 = requests.post(url=fail_txt_url())
    print('Logging failure to prodtests')
    res3 = requests.post(url=fail_logger_url(), data=report)

    if res1.status_code!=200:
        print('Failed to send email alert for some reason',flush=True)
        return False
    if res2.status_code!=200:
        print('Logging to prodtests failed for some reason',flush=True)
        return False
    if res3.status_code==200:
          print('Successfully logged failure at prodtests',flush=True)
          return True
    else:
          print('Failed to log at prodtests',flush=True)
          return False

def basic_system_checks():
    try:
        lagged = getjson('https://api.microprediction.org/live/lagged_times::three_body_z.json')
    except Exception as e:
        return [{'error':'feed down can''t get three_body','message':'Three body is stale','error_message':str(e)}]
    latency = time.time() - float(lagged[0])
    if latency>200:
        return {'error':'unusual latency for three_body_z.json','message':'Three body is stale... time since last update '+str(latency)}

def basic_failover_checks():
    try:
        lagged = getjson('https://stableapi.microprediction.org/live/lagged_times::three_body_z.json')
    except Exception as e:
        return [{'error':'STABLE API feed down can''t get three_body','message':'Three body is stale','error_message':str(e)}]
    latency = time.time() - float(lagged[0])
    if latency>200:
        return {'error':'STABLE API unusual latency for three_body_z.json','message':'Three body is stale... time since last update '+str(latency)}


class Coyote(ReportingCrawler):

    def setup(self):
        self.initial_balance = self.get_balance()
        print('Running setup checks',flush=True)
        import os
        print( os.getenv('VIRTUAL_ENV') )
        return basic_system_checks() or basic_failover_checks()

    def teardown(self):
        print('Running teardown checks',flush=True)
        self.final_balance = self.get_balance()
        if abs(float(self.final_balance)-float(self.initial_balance))<1e-5:
            teardown_errors = {'error':'inactivity','message':'Final balance is the same as initial balance',
                  'initial_balance':self.initial_balance,
                  'final_balance':self.final_balance}
            pprint(teardown_errors)
            print('Teardown not successful',flush=True)
            return teardown_errors
        else:
            print('No teardown errors',flush=True)


if __name__=="__main__":
    print(FLASHY_COYOTE)
    if len(sys.argv)>1:
        timeout=int(sys.argv[1])
    else:
        timeout = 60*10
    if len(sys.argv)>2:
        base_url = sys.argv[2]
    else:
        base_url = 'http://api.microprediction.org'
    if len(sys.argv)>3:
        write_key = sys.argv[3]
    else:
        write_key = FLASHY_COYOTE

    mw = Coyote(write_key=write_key,pass_callback=pass_callback,fail_callback=fail_callback)
    mw.base_url = base_url
    name = 'Initialized environment for '+mw.animal_from_key(write_key)+' hitting '+base_url+' w/ env '+ os.getenv('VIRTUAL_ENV')+' reporting to '+prod_or_dev()+'tests.microprediction.org'
    mw.run_and_report(timeout=timeout,name=name)


