
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


l1,l2,l3 = 1e2,1e2,1e2 # tuned mass damper damping
k1,k2,k3 = 1,1,1 # tuned mass damper stiffnesses
m1,m2,m3 = 1,1,1 # tuned mass damper masses

K1, K2, K3 = 1,1,1 # strucutre stiffnesses
L1, L2, L3 = 1,1,1 # structure damping
M1,M2,M3 = 1,1,1 # structure masses

dt = 0.001 # time step
T = np.arange(0, 20, dt) # time array

xinput = np.sin(2*np.pi*T) # input signal
dxinput = np.diff(xinput)/dt # input signal derivative
M = np.diag([M1, M2, M3, m1, m2, m3])
MI = np.linalg.inv(M)

x1, x2, x3 = 0,0,0 # initial conditions
dx1, dx2, dx3 = 0,0,0 # initial conditions
ddx1, ddx2, ddx3 = 0,0,0 # initial conditions

y1, y2, y3 = 0,0,0 # initial conditions
dy1, dy2, dy3 = 0,0,0 # initial conditions
ddy1, ddy2, ddy3 = 0,0,0 # initial conditions

x1s = []
x2s = []
x3s = []

for i,t in enumerate(T):

    xin = xinput[i]
    if i == 0:
        dxin = 0
    else:
        dxin = dxinput[i-1]

    ddx1 = ((xin - x1)*K1 + (x2 - x1)*K2 + (dxin - dx1)*L1 + (dx2 - dx1)*L2 + (y1 - x1)*k1 + (dy1 - dx1)*l1)/M1
    ddx2 = ((x1 - x2)*K2 + (x3 - x2)*K3 + (dx1 - dx2)*L2 + (dx3 - dx2)*L3 + (y2 - x2)*k2 + (dy2 - dx2)*l2)/M2
    ddx3 = ((x2 - x3)*K3 + (dx2 - dx3)*L3 + (y3 - x3)*k3 + (dy3 - dx3)*l3)/M3
    ddy1 = ((x1 - y1)*k1 + (dx1 - dy1)*l1)/m1
    ddy2 = ((x2 - y2)*k2 + (dx2 - dy2)*l2)/m2
    ddy3 = ((x3 - y3)*k3 + (dx3 - dy3)*l3)/m3

    x1 = x1 + dx1*dt + 0.5*ddx1*dt**2
    x2 = x2 + dx2*dt + 0.5*ddx2*dt**2
    x3 = x3 + dx3*dt + 0.5*ddx3*dt**2
    y1 = y1 + dy1*dt + 0.5*ddy1*dt**2
    y2 = y2 + dy2*dt + 0.5*ddy2*dt**2
    y3 = y3 + dy3*dt + 0.5*ddy3*dt**2

    dx1 = dx1 + ddx1*dt
    dx2 = dx2 + ddx2*dt
    dx3 = dx3 + ddx3*dt
    dy1 = dy1 + ddy1*dt
    dy2 = dy2 + ddy2*dt
    dy3 = dy3 + ddy3*dt

    x1s.append(x1)
    x2s.append(x2)
    x3s.append(x3)

#plt.plot(T, xinput, label='input')
plt.plot(T, x1s, label='x1')
plt.plot(T, x2s, label='x2')
plt.plot(T, x3s, label='x3')

plt.legend()
plt.show()