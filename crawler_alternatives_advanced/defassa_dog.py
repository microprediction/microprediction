

if __name__=='__main__':
    try:
        from credentials import DEFASSA_DOG, ELFEST_BOBCAT
    except ImportError:
        raise Exception('You cannot run this example unless you create your own streams')

    try:
        from winning.lattice import density_from_samples
    except ImportError:
        raise Exception('pip install winning')

    from microprediction import MicroWriter

    import random

    mw_getter = MicroWriter(write_key=ELFEST_BOBCAT)
    mw_setter = MicroWriter(write_key=DEFASSA_DOG)
    from pprint import pprint
    import math


    def arbitrage():
        for hole_no in range(1, 19):
            ability = mw_getter.get_lagged_values('tour_' + str(hole_no) + '_sg_total.json')[0]
            is_ = {'great': ability > 1.25,
                   'good': 0.5 < ability <= 1.25,
                   'okay': -0.5 < ability <= 0.5,
                   'bad': ability < 0.5}
            for thing in list(is_.keys()):
                if is_[thing]:
                    print('Hole ' + str(hole_no) + ' will be played by someone ' + thing)
                    for delay in mw_getter.DELAYS:
                        min_delay = max(delay, mw_getter.DELAYS[-2])
                        predictions = mw_getter.get_own_predictions(name='tour_' + str(hole_no) + '_' + thing + '.json',
                                                                    delay=min_delay)
                        rounded_predictions = [int(p) for p in predictions]
                        density = density_from_samples(rounded_predictions, L=3, unit=1)
                        outcomes = [-3, -2, -1, 0, 1, 2, 3]
                        print(list(zip(outcomes, density)))
                        num_samples = mw_getter.num_predictions
                        density_rounded = [int(math.ceil(num_samples * d)) for d in density]
                        too_many_samples = list()
                        for o, sc in zip(outcomes, density_rounded):
                            for _ in range(sc):
                                too_many_samples.append(o)
                        random.shuffle(too_many_samples)
                        values = sorted(too_many_samples[:num_samples])
                        res = mw_setter.submit(name='tour_' + str(hole_no) + '.json', delay=delay, values=values)
                        pprint(res)


    import time
    for _ in range(5):
        arbitrage()
        time.sleep(60*11)