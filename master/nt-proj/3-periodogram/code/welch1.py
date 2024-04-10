# welch.py

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
    N = 2000
    t_disc = np.linspace(0, 1, N)
    Ts = t_disc[1] - t_disc[0]

    signal_A = my_signal(t_disc, [(1.0, 100.5), (0.6, 199.5)])
    signal_B = my_signal(t_disc, [(0.6, 100.5), (0.6, 109.5)])

    freq_A, per_A = scipy.signal.periodogram(signal_A, fs=1/Ts)
    freq_welch_A, per_welch_A = scipy.signal.welch(signal_A, fs=1/Ts)

    freq_B, per_B = scipy.signal.periodogram(signal_B, fs=1/Ts)
    freq_welch_B, per_welch_B = scipy.signal.welch(signal_B, fs=1/Ts)


    fig = plt.figure()
    axs = fig.subplots(2, 1)
    plot_periodogram(axs[0], freq_A, per_A,
                     label="standard periodogram", color="C1")
    plot_periodogram(axs[0], freq_welch_A, per_welch_A,
                     label="welch periodogram", color="C0")
    axs[0].set_title("Periodograms of signal $A$")

    plot_periodogram(axs[1], freq_B, per_B,
                     label="standard periodogram", color="C1")
    plot_periodogram(axs[1], freq_welch_B, per_welch_B,
                     label="welch periodogram", color="C0")
    axs[1].set_title("Periodograms of signal $B$")

    for ax in axs:
        ax.legend()
    fig.suptitle("PSD estimates using different periodograms")
    fig.tight_layout()
    plt.savefig("outputs/welch.pdf")
    plt.show()

if __name__ == "__main__":
    main()
