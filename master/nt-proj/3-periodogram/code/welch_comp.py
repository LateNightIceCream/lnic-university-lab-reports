# welch_segments.py

import scipy
import numpy as np
from matplotlib import pyplot as plt


class WelchConfig:
    def __init__(self, win='hann', nperseg=None, noverlap=None):
        self.win = win
        self.nperseg = nperseg
        self.noverlap = noverlap

    def periodogram(self, data, fs):
        return \
            scipy.signal.welch(data, fs=fs,
                               window=self.win,
                               nperseg=self.nperseg,
                               noverlap=self.noverlap)

    def get_label(self):
        # cheats (only for N=2000)
        nperseg_l = 1000 if self.nperseg is None else self.nperseg
        noverlap_l = 500 if self.noverlap is None else self.noverlap
        return "window: %s, segment size: %d, overlap size: %d"\
            % (self.win, nperseg_l, noverlap_l)


def my_signal(t, param_list):
    signal = np.zeros(t.size)
    noise = np.random.normal(scale=2, size=t.size)
    for pair in param_list:
        amp = pair[0]
        freq = pair[1]
        signal += amp * np.sin(2 * np.pi * freq * t)
    return signal + noise


def main():
    N = 2000
    t_disc = np.linspace(0, 3, N)
    Ts = t_disc[1] - t_disc[0]

    signal_B = my_signal(t_disc, [(1, 100.5), (0.6, 109.5)])

    welch_configs = [
        WelchConfig('hann', 256),
        WelchConfig('hann', 128),
        WelchConfig('hann', 32),
    ]

    plt.figure()

    for config in welch_configs:
        freq_welch_B, per_welch_B = config.periodogram(signal_B, fs=1/Ts)
        plt.semilogy(freq_welch_B, per_welch_B, label=config.get_label())

    plt.ylim([10e-4, 0.2])
    plt.xlim([0, 400])
    plt.xlabel("f in Hz")
    plt.ylabel("$\widehat{PSD}$ in V$^2$/Hz")
    plt.legend()
    plt.title("Comparison of Welch-periodograms for different segment sizes")
    plt.tight_layout()
    plt.savefig("outputs/welch_comp.pdf")
    plt.show()


if __name__ == "__main__":
    main()
