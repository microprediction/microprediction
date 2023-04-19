
from getjson import getjson

def pga_contenders():
    return getjson('https://micropredictionmiscstreams.pythonanywhere.com/contenders/names')
  
  
def contender_index(player_name, contenders=None):
    if contenders is None:
      contenders = pga_contenders()
    matches = [ ndx for ndx,name in contenders.items() if name==player_name ]
    if matches:
        return matches[0]
    else:
        return -1


def contender_stream_name(contender_ndx, hole):
    return 'pga_contender_'+str(contender_ndx)+'_hole_'+str(hole)+'.json'
