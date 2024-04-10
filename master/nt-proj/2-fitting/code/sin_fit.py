# sin_fit.py

import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

# sinusoidal function
def temp_func(x, amp_temp, mean_temp, period, start_hr):
  # Amp_temp is variation of temp in a day, Mean_Temp is average of the day
  return mean_temp - amp_temp * np.cos(2*np.pi*(1/period) * (x - start_hr))

def main():
    time_hr = np.arange(0, 72, 2) # 2 hours apart for 3 days
    time_hr_cont = np.linspace(0, 72, 1000)
    original_params = (15, 13, 24, 0)
    temp_data_sim = temp_func(time_hr, *original_params)

    rng = np.random.default_rng()
    temp_noise = 3.8 * rng.normal(size=time_hr.size)
    temp_data = temp_data_sim + temp_noise

    popt, pcov = curve_fit(temp_func, time_hr, temp_data)
    popt2, pcov2 = curve_fit(temp_func, time_hr, temp_data,
                             bounds = (
                                 [-np.inf, -np.inf, 18, -np.inf],
                                 [np.inf, np.inf, 24, np.inf]
                             ))

    plt.figure()
    plt.title('Curve Fitting of Temperature Data')
    plt.scatter(time_hr, temp_data, color="C1", label='Noisy Temperature Data')
    plt.plot(time_hr_cont, temp_func(time_hr_cont, *original_params),
             color="gray",
             linestyle="dashed",
             label='original function: A=%5.3f°C, Mean=%5.3f°C, Period=%5.3fh, Start=%5.3fh'
             % tuple(original_params))
    plt.plot(time_hr_cont, temp_func(time_hr_cont, *popt),
             color="C0",
             label='fit (unbounded): A=%5.3f°C, Mean=%5.3f°C, Period=%5.3fh, Start=%5.3fh'
             % tuple(popt))
    plt.plot(time_hr_cont, temp_func(time_hr_cont, *popt2),
             color="C4",
             label='fit (bounded): A=%5.3f°C, Mean=%5.3f°C, Period=%5.3fh, Start=%5.3fh'
             % tuple(popt2))
    plt.legend()
    plt.xlabel('Time(hrs)')
    plt.ylabel('Temperature ($^\circ$C)')
    plt.savefig("outputs/sin_fit.pdf")
    plt.show()


if __name__ == '__main__':
    main()
