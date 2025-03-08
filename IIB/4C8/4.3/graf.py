import matplotlib.pyplot as plt
import numpy as np

dels = np.array([5, 10, 15])
i_data = [None] * len(dels)
iii_data = [None] * len(dels)

xcal = 12
slope = -104.935
intercept = -0.664

i_Y_ss = [0, 0, 0]
iii_Y_ss = [0, 0, 0]

xmin, xmax = 0.15, 0.8

def peak2peak(data):
    mask = (xmin < data[:, 0]) & (data[:, 0] < xmax)
    dmx = np.gradient(data[:, 0])
    return (np.mean(data[mask & (dmx > 0), 1]) - 
                np.mean(data[mask & (dmx < 0), 1])) / 2

for i, delta in enumerate(dels):
    i_data[i] = np.loadtxt(f'IIB/4C8/4.3/i_d={delta}.csv', delimiter=',')
    iii_data[i] = np.loadtxt(f'IIB/4C8/4.3/iii_d={delta}.csv', delimiter=',')

    i_data[i][:, 0] /= xcal
    iii_data[i][:, 0] /= xcal

    i_data[i][:, 1] = slope * i_data[i][:, 1] + intercept
    iii_data[i][:, 1] = slope * iii_data[i][:, 1] + intercept

    i_Y_ss[i] = peak2peak(i_data[i])
    iii_Y_ss[i] = peak2peak(iii_data[i])


fig, ax = plt.subplots(len(dels), 2, figsize=(10, 15))

for i, delta in enumerate(dels):
    ax[i, 0].plot(i_data[i][:, 0], i_data[i][:, 1], '-', label='Data')
    ax[i, 0].set_title(f'Part I: $d = {delta}$ cm')
    ax[i, 0].set_xlabel('Voltage (V)')
    ax[i, 0].set_ylabel('Force (N)')

    ax[i, 1].plot(iii_data[i][:, 0], iii_data[i][:, 1], '-', label='Data')
    ax[i, 1].set_title(f'Part III: $d = {delta}$ cm')
    ax[i, 1].set_xlabel('Voltage (V)')
    ax[i, 1].set_ylabel('Force (N)')

    ax[i, 0].grid()
    ax[i, 1].grid()

fig.tight_layout()

fig, ax = plt.subplots()

tandels = np.tan(np.deg2rad(dels))

ax.plot(tandels, i_Y_ss, 'o-', label='W=3kg')
ax.plot(tandels, iii_Y_ss, 'o-', label='W=5kg')
ax.grid()
ax.set_xlabel('$tan(\delta)$ [-]')
ax.set_ylabel('$Y_{SS}$ [-]')
ax.legend()

C22_3 = (i_Y_ss[1] - i_Y_ss[0])/(tandels[1] - tandels[0])
C22_5 = (iii_Y_ss[1] - iii_Y_ss[0])/(tandels[1] - tandels[0])

print(f'C22 = {C22_5:.3f} N')

fig.savefig('IIB/4C8/4.3/Yss_vs_tandelta.png', dpi=300)
plt.show()