from microprediction import MicroCrawler, new_key
from pprint import pprint

write_key = new_key(difficulty=8)
print(write_key)
crawler   = MicroCrawler(write_key=write_key,sleep_time=30, verbose=True )
crawler.run()

pprint(crawler.get_performance())


