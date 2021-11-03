# Things you can run to help support the overall effort
# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started creating streams and/or submitting predictions.

import requests, random
from pprint import pprint
from microprediction import new_key
import multiprocessing as mp

def donate(difficulty=None, password=None, donor='anonymous'):
    donate1(difficulty=difficulty,password=password, donor=donor)

def donaten(difficulty=None, password=None, donor='anonymous'):
    # Not stable enough
    num_procs = mp.cpu_count()
    pool = mp.Pool(8*num_procs)
    result = [ pool.apply(func=donate1,args=(difficulty,password,donor)) for _ in range(8*num_procs) ]
    pool.close()


def donate1(difficulty=None, password=None, donor='anonymous'):
    if password is None:
        try:
            from microprediction.config_private import DONATION_PASSWORD, DONOR_NAME
        except:
            raise Exception("Ask Peter for the donation password ")
    write_key = new_key(difficulty=8)
    res = requests.post('https://api.microprediction.org/donations/' + write_key,data={'password': password, 'donor': donor})
    if res.status_code==200:
        if 'password' in res.json()['message']:
            return {"error":res.json()}
        else:
            if difficulty is None:
                difficulty = random.choice([13])
            while True:
                print("Mining and donating the MUIDs with password "+password+" and donor name "+donor+". Thanks. Difficulty set to "+str(difficulty),flush=True)
                write_key = new_key(difficulty=difficulty)
                print(write_key,flush=True)
                res = requests.post('https://api.microprediction.org/donations/' + write_key, data={'password': password,'donor':donor})
                pprint(res.json())
    else:
        return res


if __name__=="__main__":
    donate(difficulty=8,password='5581cee8a281f4fd8cbe404143017046',donor='test')
