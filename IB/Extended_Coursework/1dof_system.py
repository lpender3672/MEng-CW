import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import multiprocessing as mp
from numba import jit, njit

l1 = 1 # tuned mass damper damping
k1 = 100 # tuned mass damper stiffness
m1 = 0.05 # tuned mass damper mass

K1 = 1000 # strucutre stiffness
L1 = 1 # structure damping
M1 = 1.46

dt = 0.00001
T = np.arange(0, 10, dt) # time array

wn = np.sqrt(K1/M1)
w = wn

xinput = np.sin(w*T) # input signal
dxinput = np.diff(xinput)/dt # input signal derivative

x1 = 0 # initial conditions
dx1 = 0 # initial conditions
ddx1 = 0 # initial conditions

y1 = 0 # initial conditions
dy1 = 0# initial conditions
ddy1 = 0 # initial conditions

x1s = np.zeros(len(T))

damping = True

for i,t in enumerate(T):

    xin = xinput[i]
    if i == 0:
        dxin = 0
    else:
        dxin = dxinput[i-1]

    ddx1 = ((xin - x1)*K1 + (dxin - dx1)*L1 + (y1 - x1)*k1 + (dy1 - dx1)*l1)/M1
    ddy1 = ((x1 - y1)*k1 + (dx1 - dy1)*l1)/m1
    
    x1 = x1 + dx1*dt + 0.5*ddx1*dt**2
    y1 = y1 + dy1*dt + 0.5*ddy1*dt**2
    if not damping:
        y1 = x1

    dx1 = dx1 + ddx1*dt
    dy1 = dy1 + ddy1*dt
    if not damping:
        dy1 = dx1

    x1s[i] = x1


plt.plot(T, x1s)
plt.show()
