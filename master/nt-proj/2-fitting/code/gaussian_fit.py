# gaussian_fit.py

import numpy as np
import scipy
from numpy.fft import fft, fftshift
from matplotlib import pyplot as plt
import random

# rigged discrete distribution
def rigged(size=None):
    # :)
    pool = [0, 1, 2, 3, 4, 5, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10]
    return np.random.choice(pool, size)


def gaussian_distribution(x, mean, std):
    xn = x - mean
    xn = xn / std
    return 1 / (std * np.sqrt(2.0 * np.pi)) * np.exp(-(xn ** 2) / 2.0)


def main():
    X_START = 0
    X_END = 10
    X_STEP = 1
    x_cont = np.linspace(X_START, X_END, 1000)
    x_discrete = np.arange(X_START, X_END + 1)

    data = rigged(10000)
    hist, hist_bins = np.histogram(data, bins=11, density=True)

    mean_fit, std_fit = scipy.stats.norm.fit(data)

    popt, pcov = scipy.optimize.curve_fit(gaussian_distribution, x_discrete, hist)

    plt.figure()
    plt.stem(hist, label="data histogram")
    plt.plot(x_cont, gaussian_distribution(x_cont, popt[0], popt[1]),
             label="scipy.optimize.curve_fit result: $\mu = %.2f, \sigma=%.2f$"
             % (popt[0], popt[1]), color = "C3",
             linestyle="dashed")
    plt.plot(x_cont, scipy.stats.norm.pdf(x_cont, mean_fit, std_fit),
             label="scipy.stats.norm.fit result: $\mu = %.2f, \sigma=%.2f$"
             % (mean_fit, std_fit), color = "C1")
    plt.title("Fitting the histogram with continuous PDFs")
    plt.xlabel("random value")
    plt.ylabel("probability (density)")
    plt.legend()
    plt.savefig("outputs/gauss_cont.pdf")
    plt.show()


if __name__ == '__main__':
    main()
