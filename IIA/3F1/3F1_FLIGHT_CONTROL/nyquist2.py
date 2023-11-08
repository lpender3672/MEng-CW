
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams['figure.facecolor'] = 'white'

# Define the system parameters

## 2.1 SIMPLIFIED AIRCRAFT MODEL

W = np.logspace(-10,10, 10000)

D = 0.250
T = 0.5

# G1

def Gjw1(w):
    s = 1j * w
    K = np.exp(- s * D)
    G = 2 / (T*s - 1)
    return G

#polar plot
G = Gjw1(W)
fig, ax = plt.subplots()
ax.plot(np.real(G), np.imag(G), color='blue', linewidth=1.0, label='$G_2(s)$')

# arrow
idx = np.argmin(G.imag)
x,y = G[idx].real, G[idx].imag
dx,dy = x - G[idx+1].real, y - G[idx+1].imag
ax.arrow(x, y, dx, dy, width=0.01, color = 'blue')

G = Gjw1(-W)
ax.plot(np.real(G), np.imag(G), color='blue', linewidth=1.0, linestyle='dashed')

# -w arrow
idx = np.argmax(G.imag)
x,y = G[idx].real, G[idx].imag
dx,dy = x - G[idx-1].real, y - G[idx-1].imag
ax.arrow(x, y, dx, dy, width=0.01, color = 'blue')

# G2

def Gjw2(w):
    s = 1j * w
    K = np.exp(- s * D)
    G = K* 2 / (T*s - 1)
    return G

#polar plot
G = Gjw2(W)
ax.plot(np.real(G), np.imag(G), color='orange', linewidth=1.0, label='$K(s)G_2(s)$')

# arrow
idx = np.argmin(G.imag)
x,y = G[idx].real, G[idx].imag
dx,dy = x - G[idx+1].real, y - G[idx+1].imag
ax.arrow(x, y, dx, dy, width=0.01, color = 'orange')

G = Gjw2(-W)
ax.plot(np.real(G), np.imag(G), color='orange', linewidth=1.0, linestyle='dashed')

# -w arrow
idx = np.argmax(G.imag)
x,y = G[idx].real, G[idx].imag
dx,dy = x - G[idx-1].real, y - G[idx-1].imag
ax.arrow(x, y, dx, dy, width=0.01, color = 'orange')

ax.legend()

ax.set_aspect('equal')
ax.grid(which='both')

ax.set_xlabel('Real')
ax.set_ylabel('Imaginary')
ax.set_title(f'Nyquist plot of plant $G_2(j\omega)$ with no controller')

path = "IIA/3F1/3F1_FLIGHT_CONTROL"

plt.savefig(path + '/figures/nyquist2.png', dpi=300)
plt.show()