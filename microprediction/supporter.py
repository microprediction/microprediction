# Things you can run to help support the overall effort
import requests, random
from pprint import pprint
from microprediction import new_key

try:
    from microprediction.config_private import DONATION_PASSWORD, DONOR_NAME
except:
    raise Exception("Ask Peter for the donation password ")

def donate(difficulty=None):
    if difficulty is None:
        difficulty = random.choice([12,13])
    while True:
        print("Mining and donations with password "+DONATION_PASSWORD+" and donor name "+DONOR_NAME+". Thanks. Difficulty set to "+str(difficulty))
        write_key = new_key(difficulty=12)
        print(write_key,flush=True)
        res = requests.post('https://www.microprediction.com/donations/' + write_key, data={'password': DONATION_PASSWORD,'donor':DONOR_NAME})
        pprint(res.json())


if __name__=="__main__":
    donate(difficulty=8)