from microprediction import MicroCrawler

if __name__ == '__main__':
    try:
        from microprediction.config_private import DALE_LEECH
        crawler = MicroCrawler(write_key=DALE_LEECH)
    except ImportError:
        crawler = MicroCrawler(difficulty=9)
    crawler.run()
