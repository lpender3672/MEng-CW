
import numpy as np
import matplotlib.pyplot as plt

# Define the system parameters

## 2.1 SIMPLIFIED AIRCRAFT MODEL

W = np.logspace(-10,10, 10000)

D = 0.317
T = 0.5

def Gjw(w):
    s = 1j * w
    K = np.exp(- s * D)
    G = K* 2 / (T*s - 1)
    return G

#polar plot
G = Gjw(W)
fig, ax = plt.subplots()
ax.plot(np.real(G), np.imag(G), color='blue', linewidth=1.0, label='G(s)')
G = Gjw(-W)
ax.plot(np.real(G), np.imag(G), color='blue', linewidth=1.0, label='G(s)', linestyle='dashed')

ax.set_aspect('equal')
ax.grid(which='both')

ax.set_xlabel('Real')
ax.set_ylabel('Imaginary')
ax.set_title(f'Nyquist plot of plant $G_2(j\omega)$ with controller delay {D}')

path = "IIA/3F1/3F1_FLIGHT_CONTROL"

plt.savefig(path + '/figures/nyquist3.png', dpi=300)
plt.show()