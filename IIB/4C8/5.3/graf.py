import matplotlib.pyplot as plt
import numpy as np


tvals = np.array([
    1, 2, 3
])

# i is delta = 5
# v is delta = 15
di = 5
dv = 15


circumference = 3.4 / 12 # 12 v / (v / m) = m
eff_R = circumference / (2 * np.pi)
drum_R = 74 / 2 * 1e-3
g = 9.81

droll = 12.4

xvals = tvals * g * eff_R / drum_R

i_data = [None] * len(tvals)
v_data = [None] * len(tvals)

xmin, xmax = 0.04, 0.3

def peak2peak(data):
    mask = (xmin < data[:, 0]) & (data[:, 0] < xmax)
    dmx = np.gradient(data[:, 0])
    return (np.mean(data[mask & (dmx > 0), 1]) - 
                np.mean(data[mask & (dmx < 0), 1])) / 2

i_Y_ss = [None] * len(tvals)
v_Y_ss = [None] * len(tvals)

xcal = 12
slope = -104.935
intercept = -0.664

for i, tval in enumerate(tvals):
    i_data[i] = np.loadtxt(f'IIB/4C8/5.3/T={tval}_d=5.csv', delimiter=',')
    v_data[i] = np.loadtxt(f'IIB/4C8/5.3/T={tval}_d=15.csv', delimiter=',')

    i_data[i][:, 0] /= xcal
    v_data[i][:, 0] /= xcal

    i_data[i][:, 1] = slope * i_data[i][:, 1] + intercept
    v_data[i][:, 1] = slope * v_data[i][:, 1] + intercept

    i_Y_ss[i] = peak2peak(i_data[i])
    v_Y_ss[i] = peak2peak(v_data[i])


fig, ax = plt.subplots(len(tvals), 2, figsize=(10, 15))

for i, delta in enumerate(tvals):
    ax[i, 0].plot(i_data[i][:, 0], i_data[i][:, 1], '-', label='Data')
    ax[i, 0].set_title(f'Part I: $d = {delta}$ cm')
    ax[i, 0].set_xlabel('Voltage (V)')
    ax[i, 0].set_ylabel('Force (N)')

    ax[i, 1].plot(v_data[i][:, 0], v_data[i][:, 1], '-', label='Data')
    ax[i, 1].set_title(f'Part V: $d = {delta}$ cm')
    ax[i, 1].set_xlabel('Voltage (V)')
    ax[i, 1].set_ylabel('Force (N)')

    ax[i, 0].grid()
    ax[i, 1].grid()
    
# plot X v Y

fig, ax = plt.subplots()

ax.plot(xvals, i_Y_ss, 'o-', label='d=5cm')
ax.plot(xvals, v_Y_ss, 'o-', label='d=15cm')

ax.set_xlabel('X (N)')
ax.set_ylabel('Y_ss (N)')

ax.legend()
ax.grid()

fig.savefig('IIB/4C8/5.3/XvsY.png', dpi=300)

plt.show()

# plot theoretical on top

