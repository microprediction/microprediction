from credentials import ELFEST_BOBCAT as WRITE_KEY
import requests
from microprediction.polling import MicroWriter


REPO_NAME = 'awesome-conformal-prediction'
STREAM_NAME = 'stars_awesome_conformal_prediction.json'
STREAM_URL = 'https://www.microprediction.org/stream_dashboard.html?stream=STREAM'.replace('STREAM',STREAM_NAME.replace('.json',''))

def github_stars():
    headers = {
        'Accept': 'application/vnd.github.preview',
    }

    params = {
        'q': REPO_NAME,
    }

    response = requests.get('https://api.github.com/search/repositories', params=params, headers=headers)
    return int(response.json()['items'][0]['stargazers_count'])


if __name__=="__main__":
    import time
    mw = MicroWriter(write_key=WRITE_KEY)
    prev_value = github_stars()
    start_time = time.time()
    DAY = 60*60*24
    print({'value':prev_value,'url':STREAM_URL})

    while time.time()-start_time<DAY:
        time.sleep(60*60)
        next_value = github_stars()
        change = next_value-prev_value
        mw.set(name=STREAM_NAME, value=change)
        print({'prev_value':prev_value,'next_value':next_value,'url':STREAM_URL})
        prev_value = next_value
