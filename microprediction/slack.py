import requests


# Interaction with microprediction Slack
# I'll probably move this to microconventions


def send(text, api_key):
    """
       Send text to microprediction-streams channel
    """
    data = {'text':text}
    url  = 'https://hooks.slack.com/services/' + api_key
    res = requests.put(url=url,
                       data=data)
    return res


if __name__=='__main__':
    from microprediction.config_private import SLACK_STREAMS
    text = """On Alfredo's suggestion I've added slack notifications to the microprediction client so that if you are
            very careful and sparing your crawlers can send messages to Slack. If you want to do this DM me for the
            key and then use https://github.com/microprediction/microprediction/blob/master/microprediction/slack.py              
             """
    send(text=text, api_key=SLACK_STREAMS)