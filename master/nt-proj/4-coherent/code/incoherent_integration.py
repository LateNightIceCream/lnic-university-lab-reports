# incoherent_integration.py

import scipy
import numpy as np
from numpy.fft import fft, fftshift
from matplotlib import pyplot as plt


def get_spectrum(signal, ts, ax=-1):
    # assuming signal is along columns
    if ax == -1:
        N = signal.size
    else:
        N = signal.shape[ax]
    spectrum = fft(signal, axis=ax) / N
    freq = np.fft.fftfreq(N, ts)
    freq = fftshift(freq)
    spectrum = fftshift(spectrum)
    return (freq, spectrum)


def my_signal(t, f0, fstd):
    # TODO: shape check of t
    jitter = np.random.normal(size=t.shape[0]) * fstd
    f = f0 + np.repeat(jitter[:, np.newaxis], t.shape[1], axis=1)
    Ts = t[1][1] - t[1][0]
    return 50 * np.sin(2 * np.pi * np.multiply(t, f)) * \
        scipy.signal.windows.gaussian(t.shape[1], 0.01/(Ts))


def incoherent_integration(spectra, nci):
    specs_to_avg = np.abs(spectra[0:nci])
    avg_spec = np.mean(specs_to_avg, axis=0)
    return avg_spec


def cheap_snr(spec):
    mmax = np.max(np.abs(spec))
    nmax = np.std(np.abs(spec[0:1000]))
    return (mmax / nmax) ** 2


def main():

    N = 10000  # number of samples of each realization
    R = 100  # total number of realizations
    fc = 100  # Hz
    t = np.linspace(0, 1, N)
    Ts = t[1] - t[0]

    # generate the realizations
    t = np.broadcast_to(t, (R, t.size))
    sig = my_signal(t, fc, 10)
    noise = np.random.normal(scale=15, size=(R, t.shape[1]))
    data = sig + noise

    # apply the incoherent integrations
    NCI_values = [1, 5, 10, 25, 50, 100]

    # array with all realization spectra
    freq, spectra = get_spectrum(data, Ts, ax=1)

    plt.figure()
    snr_values = []
    for nci in NCI_values:
        spec = incoherent_integration(spectra, nci)
        snr = cheap_snr(spec)
        snr_values.append(snr)
        if nci in [1, 25, 100]:
            if nci == 1:
                plt.plot(freq, np.abs(spec), label="$NCI={}$".format(nci),
                         color="lightgray")
            else:
                plt.plot(freq, np.abs(spec), label="$NCI={}$".format(nci))

    # spectrum plot
    plt.title("Incoherent Integration")
    plt.xlabel("$f$ / Hz")
    plt.ylabel("Amplitude")
    plt.xlim([-500, 500])
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/nci_spec.pdf")

    # snr plot
    plt.figure()
    plt.plot(NCI_values, snr_values, 'o-')
    plt.title("SNR vs Number of Incoherent Integrations")
    plt.xlabel("NCI")
    plt.ylabel("SNR")
    plt.tight_layout()
    plt.savefig("outputs/nci_snr.pdf")

    plt.show()


if __name__ == "__main__":
    main()
