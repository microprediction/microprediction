from microprediction.reportingcrawler import ReportingCrawler
from microprediction.config_private import dev_fail_callback, dev_pass_callback, TESTABLE_CLAM

# Runs and reports to system when things go awry

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

if __name__=="__main__":
    print(TESTABLE_CLAM)
    crawler = ReportingCrawler(write_key=TESTABLE_CLAM,pass_callback=dev_pass_callback,fail_callback=dev_fail_callback)
    crawler.run_and_report(timeout=180,name='testable clam scheduled test')
