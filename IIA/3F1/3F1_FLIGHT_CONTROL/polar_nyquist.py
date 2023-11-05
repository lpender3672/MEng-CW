
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
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

ax.plot(np.angle(G), np.abs(G), color='blue', linewidth=1.0, label='G(s)')
G = Gjw(-W)
ax.plot(np.angle(G), np.abs(G), color='blue', linewidth=1.0, label='G(s)', linestyle='dashed')

ax.set_ylim(0, 1)

plt.show()