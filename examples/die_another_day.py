from microprediction import new_key, MicroWriter

write_key       = new_key(difficulty=9)
mw              = MicroWriter(write_key=write_key)
die_rolls       = [k-2.5 for k in range(6)]*50
values          = die_rolls[:mw.num_predictions]
res             = mw.submit(name='die.json',values=values)

print('https://api.microprediction.org/home/'+write_key)


