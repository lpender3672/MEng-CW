
import numpy as np
import matplotlib.pyplot as plt

# Define the system parameters

## 2.1 SIMPLIFIED AIRCRAFT MODEL

W = np.logspace(-10,10, 10000)

k = 0.982
D = 0.333

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
G = Gjw(-W)
ax.plot(np.real(G), np.imag(G), color='blue', linewidth=1.0, label='G(s)', linestyle='dashed')

asymtope_line = np.linspace(-1, 1, 100) * 1j - k * N * (D + 1/M) / M
ax.plot(np.real(asymtope_line), np.imag(asymtope_line), color='red', linewidth=1.0, label='Asymptote', linestyle='dashed')

ax.set_xlim(-0.7, 0.2)
ax.set_ylim(-0.5, 0.5)
ax.set_aspect('equal')
ax.grid(which='both')

ax.set_xlabel('Real')
ax.set_ylabel('Imaginary')

path = "IIA/3F1/3F1_FLIGHT_CONTROL"

plt.savefig(path + '/figures/nyquist1.png', dpi=300)
plt.show()