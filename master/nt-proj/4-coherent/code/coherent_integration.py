# coherent_integration.py

import numpy as np
from matplotlib import pyplot as plt


def QAM_constellation(bits_per_symb):
    # only for even bits_per_symb
    pam = np.arange(-bits_per_symb + 1, bits_per_symb, 2)
    real = pam.repeat(bits_per_symb)
    imag = np.tile(np.hstack((pam, pam[::-1])), int(bits_per_symb) // 2)
    constellation = real + 1j * imag
    return constellation


def complex_gaussian_noise(size, std=1):
    real = np.random.normal(size=size)
    imag = np.random.normal(size=size)
    return std * (real + 1j*imag)


def my_complex_signal(bits_per_symbol, samples_per_symbol, reps=1):
    constellation = QAM_constellation(bits_per_symbol).repeat(reps)
    np.random.shuffle(constellation)
    signal = constellation.repeat(samples_per_symbol)
    return signal


def coherent_integration(time, data, ci):
    # split the data into chunks of data.size / ci
    split_data = np.array_split(data, int(np.floor(data.size / ci)))
    split_time = np.array_split(time, int(np.floor(time.size / ci)))

    # calc mean of all chunks
    data_mean = np.mean(split_data, axis=1)
    time_mean = np.mean(split_time, axis=1)

    return time_mean, data_mean


def estimate_snr_time_domain(data, actual):
    diffs = np.abs(data- actual)
    return 1 / np.mean(diffs ** 2)


def main():
    bits_per_symbol = 4 # should be even
    sig = my_complex_signal(bits_per_symbol, 50, 3)
    noise = complex_gaussian_noise(sig.size, 0.5)

    data = sig + noise

    x = np.arange(1, data.size + 1)

    ci_values = [1, 5, 10, 25, 50, 100]
    snrs_ci = []

    const_fig, const_ax = plt.subplots(1,1)
    const_ax.set_title("Noisy QAM{} constellation after CI"
                       .format(str(bits_per_symbol**2)))
    const_ax.set_xlabel("real")
    const_ax.set_ylabel("imaginary")

    time_fig, time_axs = plt.subplots(1, 1)
    time_axs.set_xlim([0, 1500])
    time_axs.set_title("Coherent Integration of Real part")
    time_axs.set_xlabel("sample index")
    time_axs.set_ylabel("real / V")

    snr_fig, snr_ax = plt.subplots(1, 1)
    snr_ax.set_title("Linear SNR vs number of integrations")
    snr_ax.set_xlabel("CI")
    snr_ax.set_ylabel("SNR (linear)")


    for ci in ci_values:

        coh_time, coh_data = coherent_integration(x, data, ci)

        # calculate CI of signal without noise
        # just to downsample it for snr calculation
        coh_time_sig, coh_data_sig = coherent_integration(x, sig, ci)

        snr = estimate_snr_time_domain(coh_data, coh_data_sig)
        snrs_ci.append(snr)

        # constellation plot
        if ci == 1:
            const_ax.scatter(np.real(coh_data), np.imag(coh_data),
                             label="$CI={}$"
                             .format(str(ci)), color="lightgray")
        else:
            const_ax.scatter(np.real(coh_data), np.imag(coh_data),
                             label="$CI={}$"
                             .format(str(ci)))

        # time plot
        if ci in [1, 25, 100]:
            if ci == 1:
                time_axs.plot(coh_time, np.real(coh_data),
                              label="$CI={}$"
                              .format(str(ci)), color="gray")
            else:
                time_axs.plot(coh_time, np.real(coh_data),
                              label="$CI={}$"
                              .format(str(ci)))

    # SNR plot
    snr_ax.plot(ci_values, snrs_ci, 'o-')

    const_ax.legend()
    time_axs.legend()

    const_fig.savefig("outputs/ci_constellation.pdf")
    time_fig.savefig("outputs/ci_real.pdf")
    snr_fig.savefig("outputs/ci_snr.pdf")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
