
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams['figure.facecolor'] = 'white'

# Define the system parameters

## 2.1 SIMPLIFIED AIRCRAFT MODEL

W = np.logspace(-10,10, 10000)

k = 1.238
D = 0.250

M = 10
N = 10


def Gjw(w):
    s = 1j * w
    K = k*np.exp(- s * D)
    G = K * N / (s**2 + M*s )
    return G

#polar plot
G = Gjw(W)
fig, ax = plt.subplots()
ax.plot(np.real(G), np.imag(G), color='blue', linewidth=1.0, label='G(s)')

# arrow
idx = np.where(np.isclose(G.imag, -0.2, atol=0.001))[0][0]
x,y = G[idx].real, G[idx].imag
dx,dy = x - G[idx+1].real, y - G[idx+1].imag
ax.arrow(x, y, dx, dy, width=0.005, color = 'blue')

G = Gjw(-W)
ax.plot(np.real(G), np.imag(G), color='blue', linewidth=1.0, label='G(s)', linestyle='dashed')

# -w arrow
idx = np.where(np.isclose(G.imag, 0.2, atol=0.001))[0][0]
x,y = G[idx].real, G[idx].imag
dx,dy = x - G[idx-1].real, y - G[idx-1].imag
ax.arrow(x, y, dx, dy, width=0.005, color = 'blue')

asymtope_value = - k * N * (D + 1/M) / M
asymtope_line = np.linspace(-1, 1, 100) * 1j + asymtope_value
ax.plot(np.real(asymtope_line), np.imag(asymtope_line), color='red', linewidth=1.0, label='Asymptote', linestyle='dashdot')

ax.set_xlim(-0.7, 0.2)
ax.set_ylim(-0.5, 0.5)
ax.set_aspect('equal')
ax.grid(which='both')

ax.text(asymtope_value-0.08, 
        ax.get_ylim()[0]+0.01, 
        f" {asymtope_value:.3f}", 
            horizontalalignment='center', 
            verticalalignment='bottom', 
            color='red')

ax.set_xlabel('Real')
ax.set_ylabel('Imaginary')
ax.set_title(f'Nyquist plot of plant, $G_1(s)$ in series with gain {k} and delay {D}')

plt.tight_layout()

path = "IIA/3F1/3F1_FLIGHT_CONTROL"

plt.savefig(path + '/figures/nyquist1.png', dpi=300)
plt.show()