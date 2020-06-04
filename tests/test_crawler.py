from microprediction import MicroCrawler, new_key

def test_crawler():
    write_key = 'a6fb60906a11113c030a4fb86db7d51b'
    crawler = MicroCrawler(write_key=write_key)
    crawler.run(timeout=3)
