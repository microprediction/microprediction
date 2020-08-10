from microprediction import SequentialStreamCrawler, SkewDist
from microprediction.config_private import FLOATABLE_BEE

if __name__=='__main__':
    crawler = SequentialStreamCrawler(write_key=FLOATABLE_BEE, machine_type=SkewDist)
    crawler.run()