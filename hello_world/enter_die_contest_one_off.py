from microprediction import new_key, MicroWriter
import random

# Get started ... just run this script once and you're good
# Video tutorials are available at https://www.microprediction.com/python-1

if __name__ == '__main__':
    print("Thanks for participating. First I need to create your identity. Be patient.")
    write_key = new_key(difficulty=10)
    mw = MicroWriter(write_key=write_key)
    
    # Create 225 guesses of the next value of a die
    die_rolls = [k - 2.5 for k in range(6)] * 50
    random.shuffle(die_rolls)
    values = sorted(die_rolls[:mw.num_predictions])
    
    # Submit them
    for delay in mw.DELAYS:
        mw.submit(name='die.json', values=values, delay=delay)
    print('Now go to https://www.microprediction.org and enter '+write_key+' into the dashboard ')

