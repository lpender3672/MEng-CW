import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


L            = 5 
x            = np.linspace(-L,L,256)
y            = np.linspace(-L,L,256)
x_mat        = np.zeros((x.size,y.size))
y_mat        = np.zeros_like(x_mat)
psi_mat      = np.zeros_like(x_mat)
psi_mat_zeta = np.zeros_like(x_mat)

# Physical constants
U     = 1.                          # freestream velocity [m/s]
R     = 1.                          # cylinder radius     [m]
alpha = np.deg2rad(10)              # freestream angle    [rad]
# Transformation constants
a     = 0.1                         # x-offset -> thickness asymmetry -> airfoil
b     = 0.1                        # y-offset -> camber -> airfoil

fig, axes = plt.subplots(5,1, gridspec_kw={'height_ratios': [10, 1, 1, 1, 1]}, figsize=(10,10))
ax = axes[0]
# set ax to be the main axes

# create matplotlib sliders for a b r on another axes

slider_a = Slider(axes[1], 'a', 0, 10, valinit=a)
slider_b = Slider(axes[2], 'b', 0, 5, valinit=b)
slider_r = Slider(axes[3], 'r', 0, 10, valinit=R)
slider_alpha = Slider(axes[4], 'alpha', 0, 2*np.pi, valinit=alpha)

def get_complex_potential(z,_U,_alpha,_a,_c):
    aa     = a*(1.+ _c)
    zz     = z+_a*_c
    zz_rot = zz*np.exp(-_alpha*1j)        # rotated complex variable zz
    circ   = -4*np.pi*aa*_U*np.sin(_alpha) # circulation (Gamma)
    return _U*zz_rot + (_U*aa**2)/zz_rot - 1j*circ*np.log(zz_rot/aa)/(2*np.pi)

def update(val):
    a = slider_a.val
    b = slider_b.val
    R = slider_r.val
    alpha = slider_alpha.val

    
def get_complex_potential(z,U,alpha,a,c):
    aa     = a*(1.+c)
    zz     = z+a*c
    zz_rot = zz*np.exp(-alpha*1j)        # rotated complex variable zz
    circ   = -4*np.pi*aa*U*np.sin(alpha) # circulation (Gamma)
    return U*zz_rot + (U*aa**2)/zz_rot - 1j*circ*np.log(zz_rot/aa)/(2*np.pi)

def update(val):
    a = slider_a.val
    b = slider_b.val
    R = slider_r.val
    alpha = slider_alpha.val
    for ix in range(x.size):
        for iy in range(y.size):
            x_mat[ix,iy] = x[ix]
            y_mat[ix,iy] = y[iy]

            z = x[ix] + 1j * y[iy]

            f_z = get_complex_potential(z,U,alpha,R,a)
            psi_mat[ix,iy] = np.imag(f_z)

            if x[ix] <= 0:
                zeta = 0.5*(z-np.sqrt(z**2-4*a**2))
            else:
                zeta = 0.5*(z+np.sqrt(z**2-4*a**2))

            f_zeta = get_complex_potential(zeta,U,alpha,R,a)
            psi_mat_zeta[ix,iy] = np.imag(f_zeta)
    
    ax.clear()
    ax.contour(x_mat,y_mat,psi_mat_zeta,256)
    ax.contour(x_mat,y_mat,psi_mat_zeta,1,colors='k',levels=[0])
    ax.set_xlim((-L,L))
    ax.set_ylim((-L,L))

    ax.set_aspect('equal', adjustable='box')



slider_a.on_changed(update)
slider_b.on_changed(update)
slider_r.on_changed(update)
slider_alpha.on_changed(update)

update(0)
plt.show()

