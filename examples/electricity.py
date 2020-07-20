from microprediction import new_key, MicroWriter
from causalens import brilliant

DARKOS_KEY = new_key(difficulty=10)
print(DARKOS_KEY)
mw = MicroWriter(write_key=DARKOS_KEY)
name = 'South_Australia_Electricity_Price.json'
lagged_values = mw.get_lagged_values(name=name)
predictions   = brilliant(lagged_values)
res = mw.submit(name=name,values=predictions,delay=910)
