from microprediction import MicroReader, MicroWriter, MicroConventions
from microprediction.config_private import FLASHY_COYOTE
import requests
from pprint import pprint


class MicroReadDocumentor(MicroConventions):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def document_get_method(self, method, arg=None, params=None):
        url = self.base_url + '/' + method
        if arg is not None:
            url = url + '/' + arg
        if params is not None:
            res = requests.get(url,params=params)
        else:
            res = requests.get(url)
        return {'url': res.url,
                'params':params,
                'body': res.request.body,
                'headers': res.headers,
                'response': res.json()}

    def _get(self):
        return self.document_get_method(method='live',arg='cop.json',params=None)

    def _leaderboard(self):
        return self.document_get_method(method='leaderboards',arg='cop.json',params={'delay':70})




if __name__=="__main__":
    rd = MicroReadDocumentor()
    print(' ----+-----')
    print('live example')
    pprint(rd._get())

    print(' ----+-----')
    print(' leaderboard example ')
    pprint(rd._leaderboard())

    for method in ['overall','sponsors','budgets','volumes','prizes','monthly','previous','prizes']:
        print(' -----+------  ')
        print('Example for '+method)
        pprint(rd.document_get_method(method=method))