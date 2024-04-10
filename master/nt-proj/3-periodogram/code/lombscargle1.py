#!/usr/bin/env python3

import scipy
import numpy as np
from matplotlib import pyplot as plt


def my_signal(t, param_list):
    signal = np.zeros(t.size)
    noise = np.random.normal(scale=1, size=t.size)
    for pair in param_list:
        amp = pair[0]
        freq = pair[1]
        signal += amp * np.sin(2 * np.pi * freq * t)
    return signal + noise


def plot_periodogram(ax, x, y, **kwargs):
    ax.semilogy(x, y, **kwargs)
    ax.set_ylim([10e-5, 1])
    ax.set_xlim([0, 400])
    ax.set_xlabel("f in Hz")
    ax.set_ylabel("$\widehat{PSD}$ in V$^2$/Hz")


def main():
    N = 600
    t_disc = np.linspace(0, 1, N)
    Ts = t_disc[1] - t_disc[0]
    # add noise to sample times
    t_noise = np.random.uniform(0, 1, N)
    t_disc_noisy = t_disc + t_noise

    signal_A = my_signal(t_disc, [(1.0, 100.5), (0.6, 199.5)])
    signal_A_uneq = my_signal(t_disc_noisy, [(1.0, 100.5), (0.6, 199.5)])

    freq_A, per_A = scipy.signal.periodogram(signal_A, fs=1/Ts)

    # rad. frequency vector at which to calculate the lomb scargle estimations
    w = np.linspace(0.01, 2*np.pi*300, 10000)
    ls_pgam = scipy.signal.lombscargle(t_disc_noisy, signal_A_uneq, w, normalize=True)

    fig = plt.figure()
    axs = fig.subplots(2, 1)
    axs[0].stem(t_disc_noisy, signal_A_uneq)
    axs[0].set_title("Unequally sampled signal $A$, $N=%s$" % (str(N)))
    axs[0].set_ylabel("$A$ in V")
    axs[0].set_xlabel("$t$ in s")
    axs[1].semilogy(freq_A, per_A, linestyle="dashed", label="equally spaced periodogram", color="C1")
    axs[1].semilogy(w/(2*np.pi), ls_pgam, color="C0", label="Lomb-Scargle periodogram")
    axs[1].set_ylim([10e-4, 1])
    axs[1].set_title("Lomb-Scargle periodogram")
    axs[1].set_ylabel("$\widehat{PSD}$ in V$^2$/Hz")
    axs[1].set_xlabel("f in Hz")

    for ax in axs:
        ax.legend()

    fig.suptitle("PSD estimate of unequally sampled time series")
    fig.tight_layout()
    plt.savefig("outputs/lomb_scargle.pdf")
    plt.show()


if __name__ == "__main__":
    main()
