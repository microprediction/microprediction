#this belongs somewhere else!
from scipy.optimize import newton

def force(x, x1, x2, m1, m2, expon=2):
    return m1 / (abs(x - x1) ** expon) - m2 / (abs(x - x2) ** 2)


def weighted_mid(x1, x2, m1, m2, expon=2):
    if x1 >= x2:
        return x1
    else:
        x_mid = 0.5*x1+0.5*x2
        x_weighted = x1 + m1/(m1+m2)**2 * (x2-x1)
        x_guess = 0.25*x_weighted+0.75*x_mid
        try:
            return newton(func=force, x0=x_guess, x1=x_mid, args=(x1, x2, m1, m2, expon), tol=(x2-x1)/100.0 )
        except:
            return x_guess
