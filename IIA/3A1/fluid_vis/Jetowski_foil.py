import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


R = 1.0
alpha = 0.0
U = 10.0

x,y = np.linspace(-10,10,100), np.linspace(-10, 10,100)
X,Y = np.meshgrid(x,y)

z = X + 1j * Y
eta = z + R**2 / z


a,b = 0,0

fig, axes = plt.subplots(5,1, gridspec_kw={'height_ratios': [10, 1, 1, 1, 1]}, figsize=(10,10))
ax = axes[0]
# set ax to be the main axes

# create matplotlib sliders for a b r on another axes

slider_a = Slider(axes[1], 'a', -1, 1, valinit=a)
slider_b = Slider(axes[2], 'b', -1, 1, valinit=b)
slider_r = Slider(axes[3], 'r', 0, 10, valinit=R)
slider_alpha = Slider(axes[4], 'alpha', 0, 2*np.pi, valinit=alpha)

def update(val):
    a = slider_a.val
    b = slider_b.val
    R = slider_r.val
    alpha = slider_alpha.val
    gamma = 4 * np.pi * U * R * (1 + a) * np.sin(alpha)
    z = X + 1j * Y
    eta = z + R**2 / z # conformal mapping
    F = U*np.exp(-1j * alpha) * (eta + R*a) + U * (R**2 * (1+a)**2) * np.exp(-1j * alpha) / (eta + R*a) + 1j * gamma / (2*np.pi) * np.log(eta + R*a)

    q = R * np.exp(-1j * np.linspace(0, 2*np.pi, 100))
    Q = q + R**2 / q

    GRAD = np.gradient(F.real)
    u,v = GRAD[1], GRAD[0]

    ax.clear()
    ax.streamplot(X,Y,u,v, color='k', density=2)
    ax.plot(Q.real, Q.imag, 'k')

    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)
    ax.set_aspect('equal')


slider_a.on_changed(update)
slider_b.on_changed(update)
slider_r.on_changed(update)
slider_alpha.on_changed(update)

update(0)
plt.show()

