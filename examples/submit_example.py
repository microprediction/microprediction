from microprediction import new_key, MicroWriter
import pprint

write_key = "ddf3b83838f7d07f0e48404115eb3ec3" or new_key(difficulty=8)
mw = MicroWriter(write_key=write_key)
name = 'cop.json'
values = [ float(x)/10.1 for x in range(mw.num_predictions) ]
res = mw.submit(name=name,values=values,delay=mw.delays[0])
pprint.pprint(res)


