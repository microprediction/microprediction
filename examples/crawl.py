from microprediction import MicroCrawler, new_key

write_key = new_key(difficulty=8)
print(write_key)
crawler   = MicroCrawler(write_key=write_key,sleep_time=3)
crawler.run()


