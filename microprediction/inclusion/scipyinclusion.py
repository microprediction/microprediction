try:
    from scipy.stats import iqr
    using_scipy = True
except ImportError:
    print('pip install --upgrade pip')
    print('pip install scipy')
    using_scipy = False