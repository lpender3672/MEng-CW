
import matplotlib.pyplot as plt
import numpy as np

# import filters from scipy
import scipy.signal as signal

# load data

data = np.loadtxt("IIB/4A4/data/acceleration_2024-12-05_12-36-30.csv", skiprows=1, delimiter=',')

time = data[:, 0]
accx, accy, accz = data[:, 1], data[:, 2], data[:, 3]

acc_total = np.sqrt(accx**2 + accy**2 + accz**2)

# plot

fig, ax = plt.subplots(1, 1, figsize=(8, 4))

#ax.plot(time, accx, label="x")
#ax.plot(time, accy, label="y")
#ax.plot(time, accz, label="z")

accxf = signal.savgol_filter(accx, 51, 3)
accyf = signal.savgol_filter(accy, 51, 3)
acczf = signal.savgol_filter(accz, 51, 3)

ax.plot(time, accxf, label="x filtered")
ax.plot(time, accyf, label="y filtered")
ax.plot(time, acczf, label="z filtered")


ax.set_xlabel("Time [s]")
ax.set_ylabel("Acceleration [m/s^2]")

plt.legend()
plt.show()