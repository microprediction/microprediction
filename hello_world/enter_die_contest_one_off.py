from microprediction import new_key, MicroWriter
from pprint import pprint

write_key = new_key(difficulty=9)
mw = MicroWriter(write_key=write_key)

# New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

if __name__ == '__main__':
    die_rolls = [k - 2.5 for k in range(6)] * 50
    values = die_rolls[:mw.num_predictions]
    pprint(mw.submit(name='die.json', values=values))
    print('https://api.microprediction.org/home/' + write_key)

