from getjson import getjson
from pprint import pprint

# Human  : "This microprediction site is confusing. I don't see who is winning what."
# Crawler: "Hold my beer ..."


def descend(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}


PRIZES = 'https://api.microprediction.org/prizes/'
pprint([list(zip(money, descend(getjson(url)))) for url, money in getjson(PRIZES).items()])


# iFrame...
# <iframe height="400px" width="100%" src="https://repl.it/@microprediction/prize-standings?lite=true" scrolling="no" frameborder="no" allowtransparency="true" allowfullscreen="true" sandbox="allow-forms allow-pointer-lock allow-popups allow-same-origin allow-scripts allow-modals"></iframe>