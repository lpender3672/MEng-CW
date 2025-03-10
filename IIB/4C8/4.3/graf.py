import matplotlib.pyplot as plt
import numpy as np

dels = np.array([5, 10, 15])
i_data = [None] * len(dels)
iii_data = [None] * len(dels)

xcal = 12
slope = -104.935
intercept = -0.664

Llever = 27
Lweel = 15.8
g = 9.81

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


Z3 = 3 * g * Llever / Lweel
Z5 = 5 * g * Llever / Lweel

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

# 2nd batch of collected data
second_batch = np.loadtxt('IIB/4C8/lateral.csv', delimiter=',', skiprows=1)
sbatc3 = second_batch[:16, :]
sbatc5 = second_batch[16:, :]
extra_dels = np.array([2.5, 7.5, 12.5])
extra_tandels = np.tan(np.deg2rad(extra_dels))
extra_Y_ss3 = np.interp(extra_tandels, np.abs(sbatc3[:,3]), sbatc3[:,7])
extra_Y_ss5 = np.interp(extra_tandels, np.abs(sbatc5[:,3]), sbatc5[:,7])
# augment the data
tandels = np.concatenate((tandels, extra_tandels))
i_Y_ss = np.concatenate((i_Y_ss, extra_Y_ss3))
iii_Y_ss = np.concatenate((iii_Y_ss, extra_Y_ss5))
# sort by tan(delta)
sort_idx = np.argsort(tandels)
tandels = tandels[sort_idx]
i_Y_ss = i_Y_ss[sort_idx]
iii_Y_ss = iii_Y_ss[sort_idx]

def plot_lin_fit(ax, xtofit, ytofit, lstyle = "-", label = ""):
    m, c = np.polyfit(xtofit, ytofit, 1)
    xlims = ax.get_xlim()
    x = np.linspace(*xlims, 100)
    flabl = f'{label} ('+'$C_{22}='+f'{m:.1f})$'
    ax.plot(x, m*x + c, lstyle, label=flabl)

npts = 3
ax.plot(tandels, i_Y_ss, 'o-', label=f'Z={Z3:.1f} measured')
plot_lin_fit(ax, tandels[:npts], i_Y_ss[:npts], '--', label=f'Z={Z3:.1f} fit')
ax.plot(tandels, iii_Y_ss, 'o-', label=f'Z={Z5:.1f} measured')
plot_lin_fit(ax, tandels[:npts], iii_Y_ss[:npts], '--', label=f'Z={Z5:.1f} fit')

ax.grid()
ax.set_xlabel('$tan(\delta)$ [-]')
ax.set_ylabel('$Y_{SS}$ [N]')
ax.legend()

fig.savefig('IIB/4C8/4.3/Yss_vs_tandelta.png', dpi=300)
plt.show()