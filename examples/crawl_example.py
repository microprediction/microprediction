from microprediction import MicroCrawler, new_key
from pprint import pprint
import muid

difficulty = 8
print('Generating MUID of difficulty '+str(difficulty)+' - please be patient')
write_key = new_key(difficulty=difficulty)
print(write_key)
print(muid.animal(write_key) + ' is starting up ')
crawler   = MicroCrawler(write_key=write_key, sleep_time=30, verbose=True )
crawler.run()

pprint(crawler.get_performance())


