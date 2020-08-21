from microprediction.writer import MicroWriter
from microprediction.set_config import MICRO_TEST_CONFIG
import requests
TEST_WRITE_KEY = MICRO_TEST_CONFIG['TEST_WRITE_KEY']
BASE_URL = MICRO_TEST_CONFIG['BASE_URLS'][1]
import json
from genson import SchemaBuilder
from microconventions import MicroConventions

# https://stackoverflow.com/questions/7341537/tool-to-generate-json-schema-from-json-data/30294535

LIST_EXAMPLES = [
    {'method':'prizes'},
    {'method':'confirms','arg':TEST_WRITE_KEY},
    {'method':'transactions','arg':TEST_WRITE_KEY}
]

DICT_EXAMPLES = [  {'method':'overall'},
    {'method':'sponsors'},
    {'method':'budgets'},
    {'method':'volumes'},
    {'method': 'monthly'},
    {'method': 'previous'}
]

def dev_get(method, arg=None, params=None):
    mc = MicroConventions(base_url='https://devapi.microprediction.org')
    url = mc.base_url + '/' + method
    if arg is not None:
        url = url + '/' + arg
    if params is not None:
        res = requests.get(url, params=params)
    else:
        res = requests.get(url)
    if res.status_code==200:
        return res.json()

def autogenerate_schemas(method, arg=None, params=None):
    mw = MicroWriter(write_key=TEST_WRITE_KEY,base_url=BASE_URL)
    obj = dev_get(method=method, arg=arg, params=params)
    if obj is not None:
        with open('./autogen_examples/'+method+'_example.json','wt') as fp:
            json.dump(fp=fp,obj=obj)
        builder = SchemaBuilder()
        seed_schema = {'type': 'array', 'items': []}
        builder.add_schema(seed_schema)
        for ob in obj:
            builder.add_object(obj=ob)
        schema = builder.to_schema()
        with open('./autogen_schemas/'+method+'_schema.json','wt') as fp:
            json.dump(fp=fp,obj=schema)
    else:
        print('Warning: '+ method + ' failed.')



if __name__== "__main__":
    for stuff in LIST_EXAMPLES:
        autogenerate_schemas(**stuff)
