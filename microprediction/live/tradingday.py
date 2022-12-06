

def yarx_moving() -> bool :
    """
        Slightly lagged proxy for the market being open
    """
    import time
    from microprediction import MicroReader
    mr = MicroReader()
    lagged_values, lagged_times = mr.get_lagged_values_and_times(name='quick_yarx_aapl.json')
    return (time.time()-lagged_times[0])<3*60*60



if __name__=='__main__':
    print({'yarx_moving':yarx_moving()})