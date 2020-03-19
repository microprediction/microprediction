from microprediction import MicroCrawler, new_key

def dont_test_crawler():
    write_key = new_key(difficulty=8)
    crawler = MicroCrawler(write_key=write_key)
    crawler.run()
