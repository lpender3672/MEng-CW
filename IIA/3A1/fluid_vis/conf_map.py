import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
# Plots streamlines using complex potentials and conformal mappings.
#------------------------------------------------------------------------------

# Computational grid
L            = 5 
x            = np.linspace(-L,L,256)
y            = np.linspace(-L,L,256)
x_mat        = np.zeros((x.size,y.size))
y_mat        = np.zeros_like(x_mat)
psi_mat      = np.zeros_like(x_mat)
psi_mat_zeta = np.zeros_like(x_mat)

# Physical constants
U     = 1.                          # freestream velocity [m/s]
a     = 1.                          # cylinder radius     [m]
alpha = np.deg2rad(10)              # freestream angle    [rad]
# Transformation constants
c     = 0.1                         # x-offset -> thickness asymmetry -> airfoil

def get_complex_potential(z,U,alpha,a,c):
    aa     = a*(1.+c)
    zz     = z+a*c
    zz_rot = zz*np.exp(-alpha*1j)        # rotated complex variable zz
    circ   = -4*np.pi*aa*U*np.sin(alpha) # circulation (Gamma)
    return U*zz_rot + (U*aa**2)/zz_rot - 1j*circ*np.log(zz_rot/aa)/(2*np.pi)

# Computes complex potentials and streamfunctions on the computational grid
for ix in range(x.size):
    for iy in range(y.size):
        x_mat[ix,iy] = x[ix]
        y_mat[ix,iy] = y[iy]

        # Complex potential for flow around cylinder as a superposition of:
        # ---------------------------------------------------------------------
        # i)   freestream @ alpha
        # ii)  doublet of strength mu (constrained so that, based on the
        #      freestream strength, the stagnation streamline forms a circle
        #      of radius a)
        # iii) circulation (Gamma) (constrained by the Kutta-Jukowski cond.)
        # ---------------------------------------------------------------------
        # Complex variable z
        z = x[ix]+(y[iy])*1j
        # Complex potential as a function of z (F(z)) defines the flow around
        # a cylinder with circulation Gamma
        f_z = get_complex_potential(z,U,alpha,a,c)
        # Imaginary component of complex potential = streamfunction
        psi_mat[ix,iy] = np.imag(f_z)
        # ---------------------------------------------------------------------

        # Transformed potential F(zeta)
        # ---------------------------------------------------------------------
        # The transformation that you are given is zeta(z) = z + a**2/z. 
        # Since we have written the complex potential as a function of z, we
        # need to find the inverse transformation. The inverse transformation is
        # found by solving a quadratic equation. It is easy to verify that:
        #
        # z = 1./2 * ( zeta +- (zeta^2-4a^2)^(1/2) )
        #
        # and you can verify, for example, that at zeta = 2a we have z = a.
        # Now as you see this equation has 2 roots, you can understand why this
        # happens if you move z around the unit circle and see how zeta moves.
        # This is why I have put this 'if' condition here below:
        if x[ix] <= 0:
            zeta = 0.5*(z-np.sqrt(z**2-4*a**2))
        else:
            zeta = 0.5*(z+np.sqrt(z**2-4*a**2))
        # Transformed complex potential F(zeta) defines flow around a flat plate
        f_zeta = get_complex_potential(zeta,U,alpha,a,c)
        psi_mat_zeta[ix,iy] = np.imag(f_zeta)

# Plotting
# ** Stagnation streamline (psi = 0) is plotted with black color **
# Streamfuction for flow around a cylinder
plt.contour(x_mat,y_mat,psi_mat,256)
plt.contour(x_mat,y_mat,psi_mat,1,colors='k',levels=[0.])
plt.xlim((-L,L)); plt.ylim((-L,L))
plt.gca().set_aspect('equal', adjustable='box'); plt.show()
# Streamfunction for flow around a flat plate
plt.contour(x_mat,y_mat,psi_mat_zeta,256)
plt.contour(x_mat,y_mat,psi_mat_zeta,1,colors='k',levels=[0])
plt.xlim((-L,L)); plt.ylim((-L,L))
plt.gca().set_aspect('equal', adjustable='box'); plt.show()
