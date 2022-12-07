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


def eastern():
    # Get the current time in Eastern Time
    eastern_time = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(-datetime.timedelta(hours=5)))

    # Format the time as a string in Snowflake-friendly format
    return eastern_time.strftime("%Y-%m-%d %H:%M:%S.%f")








if __name__=='__main__':
    print({'yarx_moving':yarx_moving()})
    print(eastern())