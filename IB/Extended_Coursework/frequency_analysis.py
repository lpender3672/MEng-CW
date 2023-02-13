
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import multiprocessing as mp
from numba import jit, njit

l1,l2,l3 = 0.1,0.1,0.1 # tuned mass damper damping
k1,k2,k3 = 1000,1000,1000 # tuned mass damper stiffnesses
m1,m2,m3 = 0.05,0.05,0.05 # tuned mass damper masses

K1, K2, K3 = 1000,1000,1000 # strucutre stiffnesses
L1, L2, L3 = 1,1,1 # structure damping
M1,M2,M3 = 1.46,1.46,1.46 # structure masses

@jit(nopython=True)
def get_maxs(w, dt):

    T = np.arange(0, 100, dt) # time array

    xinput = np.cos(w*T) # input signal
    dxinput = np.diff(xinput)/dt # input signal derivative

    x1, x2, x3 = 0,0,0 # initial conditions
    dx1, dx2, dx3 = 0,0,0 # initial conditions
    ddx1, ddx2, ddx3 = 0,0,0 # initial conditions

    y1, y2, y3 = 0,0,0 # initial conditions
    dy1, dy2, dy3 = 0,0,0 # initial conditions
    ddy1, ddy2, ddy3 = 0,0,0 # initial conditions

    x1s = np.zeros(len(T))
    x2s = np.zeros(len(T))
    x3s = np.zeros(len(T))

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

        x1s[i] = x1
        x2s[i] = x2
        x3s[i] = x3

    # get max values after initial transient period
    x1max = np.max(x1s[1000:])
    x2max = np.max(x2s[1000:])
    x3max = np.max(x3s[1000:])

    return x1max, x2max, x3max

#@njit(parallel=True)
def get_maxs_parallel(ws, dt):

    x1maxs = np.zeros(len(ws))
    x2maxs = np.zeros(len(ws))
    x3maxs = np.zeros(len(ws))

    # use multiprocessing to speed up the calculation
    pool = mp.Pool(mp.cpu_count())
    results = [pool.apply_async(get_maxs, args=(w, dt)) for w in ws]
    
    for i, result in enumerate(results):
        x1max, x2max, x3max = result.get()
        x1maxs[i] = x1max
        x2maxs[i] = x2max
        x3maxs[i] = x3max
    
    return x1maxs, x2maxs, x3maxs


if __name__ == '__main__':

    wn = np.sqrt(K1/M1)

    ws = np.linspace(wn*1e-2, wn*1e1, 100)

    dt = 0.01
    
    x1maxs, x2maxs, x3maxs = get_maxs_parallel(ws, dt=dt)

    #plt.plot(T, xinput, label='input')
    plt.plot(ws, x1maxs, label='x1 max')
    plt.plot(ws, x2maxs, label='x2 max')
    plt.plot(ws, x3maxs, label='x3 max')

    plt.legend()
    plt.show()
