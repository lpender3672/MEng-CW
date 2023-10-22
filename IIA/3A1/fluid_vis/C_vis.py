
import numpy as np
import scipy.optimize as opt
from matplotlib import pyplot as plt
from matplotlib import animation


class stream_function_visualiser_2D():

    def __init__(self, u0, map = None, psi0 = 0, type = 'cartesian'):

        self.u0 = u0
        # create psi function from u
        r = np.linspace(0, 1, 100)
        theta = np.linspace(0, 2*np.pi, 100)

        x = np.linspace(-1, 1, 100)
        y = np.linspace(-1, 1, 100)

        R, THETA = np.meshgrid(r, theta)
        #self.R = R
        #self.THETA = THETA

        if map is None:
            self.map = lambda z: z
        else:
            self.map = map

        X,Y = np.meshgrid(x, y)
        self.X = X
        self.Y = Y

        Z = X + 1j * Y
        self.Z = self.map(Z)
        self.F = u0[0] * self.Z

        self.fig, self.ax = plt.subplots()

    def add_source(self, x, y, m):
        Z = (self.X - x) + 1j * (self.Y - y)
        Z = self.map(Z)
        self.F += 1j * m / (2 * np.pi) * np.log(Z)

    def add_vortex(self, x, y, gamma):
        Z = (self.X - x) + 1j * (self.Y - y)
        Z = self.map(Z)
        self.F += gamma / (2 * np.pi) * np.log(Z)
    
    def plot(self):
        psi_grad = np.gradient(self.F)
        U = psi_grad[1].real
        V = psi_grad[0].real

        C = U**2 + V**2
        self.ax.streamplot(self.X, self.Y, U, V, color = C, density = 1, broken_streamlines=False)
        #self.ax.contour(self.X, self.Y, np.imag(self.F), 50)
        self.ax.set_aspect('equal')
        
r = 0.5
a0 = np.pi/12
c = np.exp(-1j * a0)
map = lambda z: (c*z) + r**2 / (c*z)

Vis = stream_function_visualiser_2D([5, 0], map)
Vis.add_source(0, 0, 2)
Vis.add_vortex(0, 0, 5)

Vis.plot()

plt.savefig('doublet.png')
plt.show()
