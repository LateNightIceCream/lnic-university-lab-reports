# exponential_fit.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def exponential_decrease_func(x, A, b, c):
  # A is func value at 0, b is slope of the exponent, c is offset
  return A * np.exp(-b*x) + c


def main():
    # question 2b
    time_sec = np.arange(0, 5, 0.1)
    vel_data_sim = exponential_decrease_func(time_sec, 100, 1.5, 0)

    rng = np.random.default_rng()
    vel_noise = 6.2 * rng.normal(size=time_sec.size)
    vel_data = vel_data_sim + vel_noise

    # fit the data
    popt1, pcov1 = curve_fit(exponential_decrease_func, time_sec, vel_data)

    # this is a little cheated on the bounds because the
    # max bound always has to be greater than the min bound
    popt2, pcov2 = curve_fit(exponential_decrease_func, time_sec, vel_data,
                           bounds=([-np.inf, -np.inf, 0], [np.inf, np.inf, 0.000001]))

    estimated_data1 = exponential_decrease_func(time_sec, *popt2)
    residuals1 = vel_data - estimated_data1

    plt.figure()
    y = estimated_data1
    plt.vlines(time_sec, y, y + residuals1,
               color="C2", label="Residuals to fit 2", linestyle="dashdot")
    plt.scatter(time_sec, vel_data, color="C0", label='Noisy Velocity data')
    plt.plot(time_sec, exponential_decrease_func(time_sec, *popt1), color="C4",
            label='fit 1 (unconstrained): $A=%5.3f$, $b=%5.3f$, $c=%5.3f$' % tuple(popt1))
    plt.plot(time_sec, exponential_decrease_func(time_sec, *popt2), color="C1",
            label='fit 2 (constrained $c$): $A=%5.3f$, $b=%5.3f$, $c=%5.3f$' % tuple(popt2))
    plt.legend()
    plt.xlabel('Time / sec')
    plt.ylabel('Velocity / mi/hr')
    plt.title('Curve Fitting of Exponential Velocity Data')
    plt.savefig("outputs/exp_fit.pdf")
    plt.show()


if __name__ == '__main__':
    main()
