import numpy as np
import matplotlib.pyplot as plt

# Define the system of equations
def system(x, y):
    # ddx = -3dx + 3(dx**2 x**2) * dx - x
    # turn this into a system of equations with y = dx

    return -3*y + 3*(x**2 + y**2)*y - x, x

# Create a grid of points
x = np.linspace(-2, 2, 20)
y = np.linspace(-2, 2, 20)

X, Y = np.meshgrid(x, y)

# Calculate the derivatives
u, v = np.zeros(X.shape), np.zeros(Y.shape)
NI, NJ = X.shape

for i in range(NI):
    for j in range(NJ):
        x = X[i, j]
        y = Y[i, j]
        u[i,j], v[i,j] = system(x, y)

# create contour plot
plt.streamplot(X, Y, u, v, color='black')

plt.xlabel('$x$')
plt.ylabel('$y$')
plt.title('State space quiver plot')
plt.show()