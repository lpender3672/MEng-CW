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
Llever = 27
Lweel = 15.8

xvals = tvals * g * drum_R / eff_R

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

xi = np.linspace(0, 1, 200)
mu = 0.7
C22 = 244.3
alpha5 = np.tan(np.deg2rad(5))
alpha15 = np.tan(np.deg2rad(15))

Z3 = 3 * g * Llever / Lweel
muZ = mu * Z3
xi0 = muZ / (4 * C22)

X5 = muZ * alpha5 / np.sqrt(xi**2 + alpha5**2) * (1 - xi0/(2*np.sqrt(xi**2 + alpha5**2)))
X15 = muZ * alpha15 / np.sqrt(xi**2 + alpha15**2) * (1 - xi0/(2*np.sqrt(xi**2 + alpha15**2)))

Y5 = muZ * xi / np.sqrt(xi**2 + alpha5**2) * (1 - xi0/(2*np.sqrt(xi**2 + alpha5**2)))
Y15 = muZ * xi / np.sqrt(xi**2 + alpha15**2) * (1 - xi0/(2*np.sqrt(xi**2 + alpha15**2)))

fig, ax = plt.subplots()

ax.plot(xvals, i_Y_ss, 'o-', label='$\delta=5\circ$')
ax.plot(X5, Y5, label='$\delta=5\circ$ theoretical')
ax.plot(xvals, v_Y_ss, 'o-', label='$\delta=15\circ$')
ax.plot(X15, Y15, label='$\delta=15\circ$ theoretical')

ax.set_xlabel('X (N)')
ax.set_ylabel('Y (N)')

ax.legend()
ax.grid()

fig.savefig('IIB/4C8/5.3/XvsY.png', dpi=300)

plt.show()

# plot theoretical on top

