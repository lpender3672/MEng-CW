
import numpy as np
import scipy.optimize as opt
from matplotlib import pyplot as plt
from matplotlib import animation


class stream_function_visualiser_2D():
    def __init__(self, u0, psi0 = 0, type = 'cartesian'):

        self.u0 = u0
        # create psi function from u
        r = np.linspace(0, 1, 100)
        theta = np.linspace(0, 2*np.pi, 100)

        x = np.linspace(-1, 1, 100)
        y = np.linspace(-1, 1, 100)

        R, THETA = np.meshgrid(r, theta)
        #self.R = R
        #self.THETA = THETA

        X,Y = np.meshgrid(x, y)
        self.X = X
        self.Y = Y

        self.psi = u0[0] * Y - u0[1] * X + psi0

        self.fig, self.ax = plt.subplots()

        self.sources = []
        self.vortices = []
        self.doublets = []
    
    def phi_func(self, pos):
        x = pos[0]
        y = pos[1]
        phi = self.u0[0] * pos[1] - self.u0[1] * pos[0]
        for source in self.sources:
            source_x, source_y, source_m = source
            r = np.sqrt((pos[0] - source_x)**2 + (pos[1] - source_y)**2)
            phi += source_m / (2 * np.pi) * np.log(r)

        for vortex in self.vortices:
            vortex_x, vortex_y, vortex_gamma = vortex
            theta = np.angle((pos[0] - vortex_x) + 1j * (pos[1] - vortex_y))
            phi += vortex_gamma / (2 * np.pi) * theta
        
        for doublet in self.doublets:
            pass
        print(phi.shape)
        return phi
    

    def solve_stagnant_boundary(self):
        
        x0 = np.array([0, 0])
        poss = opt.fsolve(self.phi_func, x0)

        print(poss)

    def add_source(self, x, y, m):
        # source has psi = m / 2pi * theta
        theta = np.angle((self.X - x) + 1j * (self.Y - y))
        self.psi += m * theta / (2 * np.pi)

        self.sources.append([x, y, m])

    def add_vortex(self, x, y, gamma):
        # vortex has psi = gamma / 2pi * ln(r)
        r = np.sqrt((self.X - x)**2 + (self.Y - y)**2)
        self.psi += gamma / (2 * np.pi) * np.log(r)

    def add_doublet(self, x, y, kappa):

        theta_sink = np.arctan2(self.Y - y, self.X - x)
        theta_source = np.arctan2(self.Y + y, self.X + x)

        self.psi += - kappa / (2 * np.pi) * (theta_sink - theta_source)

    def plot(self):
        psi_grad = np.gradient(self.psi)
        U,V = psi_grad[0], - psi_grad[1]

        C = U**2 + V**2
        self.ax.streamplot(self.X, self.Y, U, V, color = C, density = 1, broken_streamlines=False)


    def plot_pressure_contours(self):
        psi_grad = np.gradient(self.psi)
        U,V = psi_grad[0], - psi_grad[1]

        C = np.exp( U**2 + V**2 ) 
        self.ax.contour(self.X, self.Y, C, 5, cmap = 'autumn')

Vis = stream_function_visualiser_2D([5, 0])

#Vis.add_source(-0.2, 0, 5)

#Vis.plot()
#Vis.fill_stagnant_boundary()
Vis.add_doublet(0.5, 0, 10)
Vis.plot()

plt.savefig('doublet.png')
plt.show()
