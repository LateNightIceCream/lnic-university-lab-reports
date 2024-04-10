# constellation.py

import numpy as np
from matplotlib import pyplot as plt


def QAM_constellation(bits_per_symb):
    # only for even bits_per_symb
    pam = np.arange(-bits_per_symb + 1, bits_per_symb, 2)
    real = pam.repeat(bits_per_symb)
    imag = np.tile(np.hstack((pam, pam[::-1])), int(bits_per_symb) // 2)
    return real + 1j * imag


def complex_gaussian_noise(size, std=1):
    real = np.random.normal(size=size)
    imag = np.random.normal(size=size)
    return std * (real + 1j*imag)


def my_complex_signal(bits_per_symbol, samples_per_symbol, reps=1):
    constellation = QAM_constellation(bits_per_symbol).repeat(reps)
    np.random.shuffle(constellation)
    signal = constellation.repeat(samples_per_symbol)
    return signal


def main():
    bits_per_symbol = 4 # should be even
    sig = my_complex_signal(bits_per_symbol, 50, 3)
    noise = complex_gaussian_noise(sig.size, 0.5)

    data = sig + noise

    constellation = QAM_constellation(bits_per_symbol)

    plt.figure()
    plt.scatter(data.real, data.imag,
                label="Noisy Constellation",
                color="C1")
    plt.scatter(constellation.real, constellation.imag,
                label="Original Constellation",
                color="C0", marker="D")
    plt.xlabel("real")
    plt.ylabel("imaginary")
    plt.title("Noisy QAM{} constellation".format(str(bits_per_symbol**2)))
    plt.legend()
    plt.savefig("outputs/constellation.pdf")
    plt.show()


if __name__ == "__main__":
    main()
