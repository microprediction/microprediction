from microprediction.fitcrawler import FitCrawler
from microprediction.univariate.expnormdist import ExpNormDist
from microprediction.config_private import YEX_CHEETAH

class RegularPrizeCrawler(FitCrawler):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def include_sponsor(self,sponsor=None,**ignore):
        """ Only enter the contests with september prizes """
        return sponsor=='Emblossom Moth' or sponsor == 'Cellose Bobcat'

    def include_stream(self, name=None, **ignore):
        """ Include three_body as well, as it should do well there """
        return '~' not in name and ( 'btc_' in name or 'three_body' in name or 'c5_' in name)


if __name__ == '__main__':
    crawler = RegularPrizeCrawler(write_key=YEX_CHEETAH, machine_type=ExpNormDist, max_evals=10, min_seconds=20, min_elapsed=60, max_active=20)
    crawler.delete_performance()
    crawler.set_repository(url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/yex_cheetah.py')
    crawler.run()
