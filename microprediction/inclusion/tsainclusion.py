try:
    from timemachines.skaters.tsa.tsaensembles import tsa_precision_combined_ensemble
    using_tsa = True
except ImportError:
    print('pip install --upgrade pip')
    print('pip install timemachines')
    using_tsa = False