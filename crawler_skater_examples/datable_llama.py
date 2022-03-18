
# Datable Llama
# -------------
# Running this script is a brilliant alternative to bitcoin mining, and much more lucrative.
#
# By modifying YOUR_EMAIL you will become eligible for a daily cash prize
# See https://www.microprediction.com/competitions for more details.
#
# This is an example of:
#     A crawler (see below)
#        That uses a "skater" f (from the timemachines package) to estimate future mean and std
#           And restricts its attention to certain streams relating to the FAANG stocks
#              And further restricts its attention to the longer prediction horizons (15 mins and 1hr)
#
# A "crawler" is a descendent of the MicroCrawler class that:
#        watches https://www.microprediction.org/stream_dashboard.html?stream=gnaaf_00113 and other streams
#           maintains a manifest of when and what to predict
#                 grabs lagged data values using api.microprediction.org
#                      submits 225 guesses of future values
#
# A sentient data scientist can also improve the accuracy of the predictions, naturally.


# Step 0: Modify these
YOUR_EMAIl='pcotton@intechinvestments.com'
YOUR_URL_TO_APPEAR_ON_LEADERBOARD= 'https://github.com/microprediction/microprediction/blob/master/crawler_skater_examples/seccable_llama.py'


if __name__=='__main__':

    # Step 1: We need a WRITE_KEY, but only the first time this is run
    try:
        from credentials import DATABLE_LLAMA as WRITE_KEY
    except ImportError:
        print('You need to supply a WRITE_KEY somehow')
        print('I''m creating one for you now ... if you are very patient (go for a jog).')
        print('But I suggest you exit out of the script and read https://www.microprediction.com/private-keys for instructions and do this offline')
        print('Or maybe hassle us in Slack if you are impatient and do not wish to wait for the key to burn. See the invite at https://github.com/microprediction')
        from microconventions import new_key
        WRITE_KEY = new_key(difficulty=11)
        print(WRITE_KEY)
        print('Do not lose that key!')


    # Step 2: We need a skater "f"
    # See https://github.com/microprediction/timemachines for more explanation, and choices of "f"
    try:
        from timemachines.skaters.simple.movingaverage import precision_ema_ensemble as f
    except ImportError:
        print('pip install --upgrade pip')
        print('pip install timemachines')
        raise EnvironmentError

    # Step 3: We need a fairly recent version of microprediction client
    try:
        from microprediction.streamskater import RegularFaangStreamSkater
    except ImportError:
        print('pip install --upgrade pip')
        print('pip install --upgrade microprediction')
        raise EnvironmentError

    # Step 4: Run the crawler!
    use_mean = True  # The skater will influence the mean of the 225 guesses provided
    use_std = True   # The skater will influence the std of the 225 guesses provided
    max_active = 200 # Use this to limit the number of streams it tries to predict

    skater = RegularFaangStreamSkater(write_key=WRITE_KEY, f=f, use_mean=use_mean, use_std=use_std, max_active=max_active)
    skater.set_repository(YOUR_URL_TO_APPEAR_ON_LEADERBOARD)
    skater.set_email(YOUR_EMAIl)
    skater.run()
