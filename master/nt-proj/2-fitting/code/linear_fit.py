# linear_fit.py

import numpy as np
import scipy
from numpy.fft import fft, fftshift
from matplotlib import pyplot as plt
import random


def fit_linear_least_squares_diy(x, y):
    # equations can be found at
    # https://mathworld.wolfram.com/LeastSquaresFitting.html
    n = len(x)
    x_sum = np.sum(x)
    x_squared_sum = np.sum(x ** 2)
    y_sum = np.sum(y)
    prod_sum = np.inner(x,y)

    A_mat = np.array([[n, x_sum], [x_sum, x_squared_sum]])
    B_mat = np.array([[y_sum], [prod_sum]])
    ab = np.matmul(np.linalg.inv(A_mat), B_mat)

    return (ab[0][0], ab[1][0])


def get_velocity_profile(a, v0):
    return lambda t: velocity(t, a, v0)


def velocity(t, a, v0):
    return -a * t + v0


def velocity_noise(length):
    return 3.8 * (np.random.normal(size=length))


def main():

    T_START = 0
    T_END = 10
    T_STEP = 1
    t_cont = np.linspace(T_START, T_END, 1000)
    t_discrete = np.linspace(T_START, T_END, 30)

    # generate random function parameters
    rand_accel = random.uniform(1.0, 10.0)
    rand_v0 = random.uniform(1.0, 10.0)

    # original values
    actual_velocity_fun = get_velocity_profile(rand_accel, rand_v0)
    actual_values = actual_velocity_fun(t_discrete)

    # add noise
    noisy_values = actual_values + velocity_noise(len(actual_values))

    # DIY approach
    est_v0, est_accel = fit_linear_least_squares_diy(t_discrete, noisy_values)
    est_accel = -est_accel
    estimated_velocity_fun = get_velocity_profile(est_accel, est_v0)

    # scipy approach
    popt, pcov = scipy.optimize.curve_fit(velocity, t_discrete, noisy_values)
    scipy_velocity_fun = get_velocity_profile(popt[0], popt[1])

    # calc residuals
    residuals = noisy_values - estimated_velocity_fun(t_discrete)

    # plotting
    # plot points and functions
    plt.figure()
    plt.scatter(t_discrete, noisy_values, color="C2")
    plt.plot(t_cont, actual_velocity_fun(t_cont),
             linestyle="dotted", color="gray",
             label="original function witout noise")
    plt.plot(t_cont, estimated_velocity_fun(t_cont),
             label="DIY estimated velocity function",
             color="C1")
    plt.plot(t_cont, scipy_velocity_fun(t_cont),
             linestyle="dashed", color="C0",
             label="scipy estimated velocity function")
    # plot residual lines
    y = estimated_velocity_fun(t_discrete)
    plt.vlines(t_discrete, y, y + residuals,
               color="C2", label="residuals", linestyle="dashdot")

    plt.legend()
    plt.suptitle("Linear Fit for Constant Acceleration Model")
    plt.title("Actual parameters (no noise): $a = "
              + str(round(-rand_accel, 2))
              + ", v_0 = " + str(round(rand_v0, 2))
              + "$\nEstimated parameters: $a = "
              + str(round(-est_accel, 2))
              + ", v_0 = " + str(round(est_v0, 2)) +
              "$")
    plt.xlabel("$t$ / s")
    plt.ylabel("$v$ / m/s")

    plt.savefig("outputs/linear_fit.pdf")

    plt.show()


if __name__ == '__main__':
    main()
