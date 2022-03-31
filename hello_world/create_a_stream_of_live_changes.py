from microprediction.polling import ChangePoll
from microprediction import new_key


def func():
    """
       The quantity of interest, typically a live measurement
    """
    from microprediction.live import verrazano_speed
    return verrazano_speed()


if __name__=="__main__":
    WRITE_KEY = new_key(difficulty=12)          # <--- Could take many hours, sorry
    poller = ChangePoll(write_key=WRITE_KEY,
                        name='my_stream.json',  # <-- Name of the stream must end in .json
                        interval=10,            # <-- Publish change every 10 minutes
                        func=func)
    poller.run()
