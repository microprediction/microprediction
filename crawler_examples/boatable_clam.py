# Example of using the package echochamber, which in turn uses MicroCrawler
# This crawls www.microprediction.org, as explained by the helper site www.microprediction.com
# Need help? New video tutorials are available at https://www.microprediction.com/python-1 to help you
# get started running crawlers at www.microprediction.com

try:
    from microprediction.config_private import BOATABLE_CLAM
except ImportError:
    raise Exception('You will need a write key. See https://www.microprediction.com/private-keys')

try:
    from echochamber import EchoCrawler
except ImportError:
    raise Exception('You will need to pip install echochamber for this example to work')


# Poke around https://github.com/microprediction/echochamber/blob/master/echochamber/crawler.py
# to see what this is doing. Some parameters to the Echo state network are:

# Feel free to mess with these or hyperoptimize
PARAMS = {'n_reservoir':25,        # ECN default 200
          'sparsity':0,            # Default 0
          'spectral_radius':0.95,  # Default 0.95
          'noise':0.002}           # Default 0.001

# Maybe you want this if you want to see if recent performance is trending in the right direction.
RESET_PERFORMANCE_ON_RESTART=True


class CryptoEchoCrawler(EchoCrawler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def candidate_streams(self):
        return [name for name in self.get_streams() if 'c5_' in name or 'btc_' in name or 'three_body' in name]


if __name__=='__main__':
    crawler = CryptoEchoCrawler(write_key=BOATABLE_CLAM, **PARAMS)

    if RESET_PERFORMANCE_ON_RESTART:
        crawler.delete_performance()

    crawler.set_repository(url='https://github.com/microprediction/microprediction/blob/master/crawler_examples/boatable_clam.py')
    crawler.set_email("me@gmail.com")  # Only used to send you a voucher if you win a daily prize
    crawler.run()






    # -- ESN_PARAMS --
    #        n_reservoir: nr of reservoir neurons
    #        spectral_radius: spectral radius of the recurrent weight matrix
    #        sparsity: proportion of recurrent weights set to zero
    #        noise: noise added to each neuron (regularization)
    #        input_shift: scalar or vector of length n_inputs to add to each
    #                    input dimension before feeding it to the network.
    #        input_scaling: scalar or vector of length n_inputs to multiply
    #                    with each input dimension before feeding it to the netw.
    #        teacher_forcing: if True, feed the target back into output units
    #        teacher_scaling: factor applied to the target signal
    #        teacher_shift: additive term applied to the target signal
    #        out_activation: output activation function (applied to the readout)
    #        inverse_out_activation: inverse of the output activation function
    #        random_state: positive integer seed, np.rand.RandomState object,
    #                      or None to use numpy's builting RandomState.
    #        silent: suppress messages
