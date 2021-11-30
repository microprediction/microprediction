from microprediction import new_key, MicroWriter
from pprint import pprint

# The absolute quickish way to enter a contest ... just run this script once and you're good
# Video tutorials are available at https://www.microprediction.com/python-1

if __name__ == '__main__':
    write_key = new_key(difficulty=9)
    mw = MicroWriter(write_key=write_key)
    die_rolls = [k - 2.5 for k in range(6)] * 50
    values = die_rolls[:mw.num_predictions]
    pprint(mw.submit(name='die.json', values=values))
    print('https://api.microprediction.org/home/' + write_key)

    print('Now go to https://www.microprediction.org and enter '+write_key+' into the dashboard ')

