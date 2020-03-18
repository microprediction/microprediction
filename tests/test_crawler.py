from microprediction import MicroCrawler, new_key

def test_crawler():
    write_key = new_key()
    crawler = MicroCrawler(write_key=write_key)
    crawler.run()
