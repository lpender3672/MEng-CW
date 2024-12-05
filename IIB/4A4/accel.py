
import matplotlib.pyplot as plt
import numpy as np


# load data

data = np.loadtxt("IIB/4A4/data/acceleration_2024-12-05_12-36-30.csv", skiprows=1, delimiter=',')

time = data[:, 0]
accx, accy, accz = data[:, 1], data[:, 2], data[:, 3]

acc_total = np.sqrt(accx**2 + accy**2 + accz**2)

# plot

fig, ax = plt.subplots(1, 1, figsize=(8, 4))

ax.plot(time, accx, label="x")
ax.plot(time, accy, label="y")
ax.plot(time, accz, label="z")
ax.set_xlabel("Time [s]")
ax.set_ylabel("Acceleration [m/s^2]")

plt.legend()
plt.show()