import os
from getjson import getjson
from microprediction import MicroWriter

# This is a 'bare-bones' example of using MicroWriter.set(name=, value=)
# To be used with cron or some scheduler
# You might also consider use of ChangePoll or Poll,
# (See  https://github.com/microprediction/microprediction/blob/master/stream_examples_traffic )


WRITE_KEY = os.environ.get(
    'WRITE_KEY')  # Or get your key somehow. See https://www.microprediction.com/private-keys
mw = MicroWriter(write_key=WRITE_KEY)
assert mw.key_difficulty(mw.write_key) >= 12, "You need a key of difficulty 12 to create a stream"

# Active players
ACTIVE = {'chess_blitz': {'Hikaru': 'hikaru_nakamura',
                          'Firouzja2003': 'alireza_firouzja',
                          'nihalsarin': 'nihal_sarin',
                          'DanielNaroditsky': 'daniel_naroditsky',
                          'FarOctopus': 'morgan_lu'
                          },
          'chess_bullet': {'Hikaru': 'hikaru_nakamura',
                           'Firouzja2003': 'alireza_firouzja',
                           'DanielNaroditsky': 'daniel_naroditsky',
                           'penguingm1': 'andrew_tang',
                           'wonderfultime': 'tuan_minh_le',
                           'PinIsMightier': 'peter_cotton',
                           'FarOctopus': 'morgan_lu'
                           }
          }

URL_TEMPLATE = 'https://api.chess.com/pub/player/HANDLE/stats'
CATEGORIES = ['chess_blitz', 'chess_bullet']

if __name__ == '__main__':
    for category in CATEGORIES:
        for handle, player in ACTIVE[category].items():
            url = URL_TEMPLATE.replace('HANDLE', handle.lower())
            data = getjson(url)
            if data is not None:
                current_value = int(data[category]['last']['rating'])
                level_name = category + '_level_' + handle + '.json'  # Name of stream with rating level
                previous_value = mw.get_current_value(name=level_name)
                if previous_value is None:
                    print('No previous value for ' + level_name)
                    print(mw.set(name=level_name, value=current_value))
                else:
                    if int(float(previous_value)) != int(float(current_value)):
                        print(mw.set(name=level_name, value=current_value))
                        print(level_name + ' updated to ' + str(current_value))
                    else:
                        print((level_name, current_value, ' is unchanged'))
            else:
                print(url)

