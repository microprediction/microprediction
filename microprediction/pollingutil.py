import datetime


def seconds_until_next_half_hour():
    current_time = datetime.datetime.now()
    return 30*60-(current_time.minute * 60 + current_time.second) % 1800
