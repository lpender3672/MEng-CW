import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import bode

# When this is imported, suppress warnings about too many figures being open
# to avoid scaring students!
plt.rcParams.update({'figure.max_open_warning': 0})

def plot_flight(results):
    time, error, control = results
    fig, ax = plt.subplots()
    if len(time) == 0:
        print("Results object was empty")
        return plt, ax
    ax.hlines(0, time[0], time[-1], colors='black')
    ax.plot(time, error, color='tab:blue', label='e(t)')
    ax.plot(time, control, color='tab:orange', label='u(t)')
    ax.set_xlabel("t (s)")
    ax.grid()
    ax.legend(fontsize=12)
    ax.set_xlim(time[0], time[-1])
    return plt, ax


def plot_bode_diagram(plant, gain, delay, f_min=0.1, f_max=10):
    W = np.logspace(np.log10(f_min), np.log10(f_max), num=500)
    W, magnitude, phase = bode(plant, W)

    # gain is a constant vertical translation
    gain_in_dbs = 20 * np.log10(gain)
    magnitude_with_gain = magnitude + gain_in_dbs

    # phase is a translation vetically as a function of frequency
    phase_from_delays = np.array(
        [np.angle(np.exp(-1.0j*w*delay), deg=True) for w in W])

    # make phase continuous:
    # i.e. if the phase jumps from -175 to +175, the phase
    # should actually be -185
    last_p = 0
    offsets = np.zeros_like(phase_from_delays)
    for i, p in enumerate(phase_from_delays):
        difference = p - last_p
        if difference > 180:
            offsets[i:] += 1
        last_p = p
    phase_from_delays = phase_from_delays - 360 * offsets
    phase_with_delays = phase + phase_from_delays

    # Render the plot
    fig, axs = plt.subplots(2, 1, sharex=True, sharey=False)

    axs[0].semilogx(W, magnitude_with_gain, color='black')
    axs[0].set_ylabel("Magnitude (dB)")
    axs[1].semilogx(W, phase_with_delays, color='black')
    axs[1].set_ylabel("Phase (deg)")
    axs[1].set_xlabel("Frequency (rad/s)")
    for ax in axs:
        ax.grid(which='both')
        ax.set_xlim(np.min(W), np.max(W))

    # Make phase ticks come in increments of a multiple of 90
    min_phase = np.min(phase_with_delays)
    ticks = np.arange(-90, min_phase, -90)
    i = 1
    while len(ticks) > 8:
        i += 1
        ticks = np.arange(-90, min_phase, -90 * i)
    axs[1].set_yticks(ticks)
    fig.suptitle(f"Plant in series with gain {gain} and delay {delay}")

    return plt, axs[0], axs[1]


def annotate_line_h(ax, value, color='blue'):
    ax.axhline(value, color=color)
    ax.text(ax.get_xlim()[
            1], value, f" {value}", horizontalalignment='left', verticalalignment='center', color=color)


def annotate_line_v(ax, value, color='blue'):
    ax.axvline(value, color=color)
    ax.text(value, ax.get_ylim()[
            1], f" {value}", horizontalalignment='center', verticalalignment='bottom', color=color)


def annotate_bode_line_v(magnitude_ax, phase_ax, value, color='green'):
    magnitude_ax.axvline(value, color=color)
    phase_ax.axvline(value, color=color)
    magnitude_ax.text(value, magnitude_ax.get_ylim()[1], f" {value}", horizontalalignment='center', verticalalignment='bottom', color=color)

def annotate_point(ax, x, y, color='red'):
    ax.scatter(x, y, color=color, s=5.0)
    if y > 0:
        text_y = y * 1.02
    elif y < 0:
        text_y = y * 0.98
    else:
        text_y - y
    ax.text(x, text_y, f"({x},{y})", color=color, horizontalalignment='left', verticalalignment='bottom')

def plot_nyquist_diagram(plant, gain, delay):

    W = np.logspace(-5, 5, num=500)
    W, magnitude, phase = bode(plant, W)

    # gain is a constant vertical translation
    gain_in_dbs = 20 * np.log10(gain)
    magnitude_with_gain = magnitude + gain_in_dbs

    # phase is a translation vetically as a function of frequency
    phase_from_delays = np.array(
        [np.angle(np.exp(-1.0j*w*delay), deg=True) for w in W])

    # make phase continuous:
    # i.e. if the phase jumps from -175 to +175, the phase
    # should actually be -185
    last_p = 0
    offsets = np.zeros_like(phase_from_delays)
    for i, p in enumerate(phase_from_delays):
        difference = p - last_p
        if difference > 180:
            offsets[i:] += 1
        last_p = p
    phase_from_delays = phase_from_delays - 360 * offsets
    phase_with_delays = phase + phase_from_delays

    # Render the plot
    # create polar plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    Z = magnitude_with_gain * np.exp(1.0j * phase_with_delays * np.pi / 180)
    ax.plot(Z.real, Z.imag, color='black')
    
    ax.grid(which='both')
    ax.set_xlim(np.min(W), np.max(W))

    
    # Make phase ticks come in increments of a multiple of 90
    fig.suptitle(f"Plant in series with gain {gain} and delay {delay}")

    return plt, ax