import numpy as np
from microconventions import discrete_pdf


def test_discrete():
    # Generate a PDF.
    # Calculate the likely CDF that will be returned.
    # Imply a PDF
    #
    # https://gist.github.com/microprediction/ea63388c2bbcfd7623bd9937723565b9
    num = 7
    cij = [[1.0] * k + [0.5] + [0.] * (num - k - 1) for k in range(num)]
    C = np.array(cij)
    probs = np.random.rand(7)
    probs = probs / sum(probs)
    cdf = np.matmul(C, np.transpose(np.array(probs)))
    pdf = discrete_pdf(ys=cdf)
    assert all([abs(p1 - p2) < 1e-5 for p1, p2 in zip(probs, pdf)])


