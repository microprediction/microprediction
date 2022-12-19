import datetime

def yarx_moving() -> bool :
    """
        Slightly lagged proxy for the market being open
    """
    import time
    from microprediction import MicroReader
    mr = MicroReader()
    lagged_values, lagged_times = mr.get_lagged_values_and_times(name='quick_yarx_aapl.json')
    return (time.time()-lagged_times[0])<10*60


def eastern(as_str=True):
    # Get the current time in Eastern Time
    from pytz import timezone
    eastern_zone = timezone('US/Eastern')
    eastern_time = datetime.datetime.now(eastern_zone)
    return eastern_time.strftime("%Y-%m-%d %H:%M:%S.%f") if as_str else eastern_time


def relative_to_4pm():
    today_4pm = datetime.datetime.combine(datetime.date.today(),datetime.time(hour=16))
    dt = eastern(as_str=False).replace(tzinfo=None) - today_4pm
    return dt


def is_near_4pm_eastern(mins=5, seconds=0):
    return abs(relative_to_4pm().total_seconds())<60*mins+seconds


def seconds_until_next_half_hour():
    current_time = datetime.datetime.now()
    return 30*60-(current_time.minute * 60 + current_time.second) % 1800



if __name__=='__main__':
    print(relative_to_4pm().total_seconds())
    print(is_near_4pm_eastern())











if __name__=='__main__':
    print({'yarx_moving':yarx_moving()})
    print(eastern())
