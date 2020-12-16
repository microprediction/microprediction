from microprediction import MicroCrawler

if __name__ == '__main__':
    try:
        from microprediction.config_private import DALE_LEECH
        crawler = MicroCrawler(write_key=DALE_LEECH)
    except ImportError:
        crawler = MicroCrawler(difficulty=11)
    crawler.set_repository(url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/dale_leech.py')
    crawler.run()
