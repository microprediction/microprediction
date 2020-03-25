from microprediction import MicroCrawler, new_key

def test_crawler():
    write_key = new_key(difficulty=8)
    crawler = MicroCrawler(write_key=write_key)
    streams = crawler.get_budgets()
    crawler.run()
