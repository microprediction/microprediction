from microprediction import MicroWriter, new_key
import random
from pprint import pprint
from collections import Counter

# Crush the die.json contest and some others using the new discrete_pdf_lagged functionality

NAMES = ['die.json']

if __name__ == "__main__":
    write_key = new_key(difficulty=8)
    print(write_key)
    mw = MicroWriter(write_key=write_key, base_url='https://devapi.microprediction.org')
    for name in NAMES:
        for delay in mw.DELAYS:
            lagged_values = mw.get_lagged_values(name=name)
            pdf = mw.get_discrete_pdf_lagged(name=name, delay=mw.DELAYS[1],
                                             lagged_values=lagged_values)  # "market measure"
            empirical_pdf = Counter(lagged_values)
            market_pdf = dict(zip(pdf['x'], pdf['y']))
            weights = [empirical_pdf[x] / (0.01 + market_pdf[x]) for x in pdf['x']]
            samples = random.choices(population=pdf['x'], weights=weights, k=mw.num_predictions)
            res = mw.submit(name=name, delay=delay, values=samples, verbose=True)
            pprint(res)
    print('Punch ' + write_key + ' into dashboard at https://www.microprediction.org/dashboard.html')
