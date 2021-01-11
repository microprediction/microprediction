import os
from getjson import getjson
from microprediction import MicroWriter

# This code lies at https://github.com/microprediction/chess/blob/main/set.py
# and generates streams such as https://www.microprediction.org/stream_dashboard.html?stream=chess_bullet_level_Hikaru


write_key = os.environ.get('WRITE_KEY')    # GitHub action needs to set env variable. You need to create a GitHub secret called WRITE_KEY
mw = MicroWriter(write_key=write_key)
assert mw.key_difficulty(mw.write_key)>=12, "You need a key of difficulty 12 to create a stream"

PLAYERS = {'Hikaru': 'hikaru_nakamura',
           'Firouzja2003': 'alireza_firouzja',
           'GMWSO': 'wesley_so',
           'LyonBeast': 'maxime_vachier_lagrave',
           'nihalsarin': 'nihal_sarin',
           'DanielNaroditsky': 'daniel_naroditsky',
           'PinIsMightier': 'halloween_gambit'}

URL_TEMPLATE = 'https://api.chess.com/pub/player/HANDLE/stats'
CATEGORIES = ['chess_blitz', 'chess_bullet']

if __name__ == '__main__':
    for category in CATEGORIES:
        for handle, player in PLAYERS.items():
            url = URL_TEMPLATE.replace('HANDLE', handle.lower())
            data = getjson(url)
            if data is not None:
                current_value = int(data[category]['last']['rating'])
                level_name = category + '_level_'  + handle + '.json'         # Name of stream with rating level
                print( (level_name, current_value, mw.set(name=level_name,value=current_value) ) )
                try:
                    previous_value = int(mw.get_current_value(name=level_name))
                except:
                    previous_value = None                       # Might not exist yet
                if previous_value is not None:
                    if int(previous_value) != int(current_value):
                        # Somebody's been playing chess
                        change_value = current_value - previous_value
                        change_name = level_name.replace('_level_','_change_')
                        print( (change_name, change_value, mw.set(name=change_name,value=change_value) ) )
            else:
                print(url)
