import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import multiprocessing as mp
from numba import jit, njit


K1 = 1000 # strucutre stiffness
L1 = 1 # structure damping
M1 = 1.46

l1 = 0.1 # tuned mass damper damping
m1 = 0.05 # tuned mass damper mass
k1 = m1 * K1 / M1 # tuned mass damper stiffness

@jit(nopython=True)
def get_maxs(w, dt, damped = False, damping = 1, stiffness = 100):
    
    T = np.arange(0, 10 * 2 * np.pi / w, dt) # time array

    xinput = np.cos(w*T) # input signal
    dxinput = np.diff(xinput)/dt # input signal derivative

    x1 = 0 # initial conditions
    dx1 = 0 # initial conditions
    ddx1 = 0 # initial conditions

    y1 = 0 # initial conditions
    dy1 = 0# initial conditions
    ddy1 = 0 # initial conditions

    x1s = np.zeros(len(T))

    for i,t in enumerate(T):

        xin = xinput[i]
        if i == 0:
            dxin = 0
        else:
            dxin = dxinput[i-1]

        ddx1 = ((xin - x1)*K1 + (dxin - dx1)*L1 + (y1 - x1)*stiffness + (dy1 - dx1)*damping)/M1
        ddy1 = ((x1 - y1)*k1 + (dx1 - dy1)*l1)/m1
        

        x1 = x1 + dx1*dt + 0.5*ddx1*dt**2
        y1 = y1 + dy1*dt + 0.5*ddy1*dt**2
        if not damped:
            y1 = x1

        dx1 = dx1 + ddx1*dt
        dy1 = dy1 + ddy1*dt
        if not damped:
            dy1 = dx1

        x1s[i] = x1

    # get max values after initial transient period
    x1max = np.max(x1s[:int(10/dt)])

    return x1max

#@njit(parallel=True)
def get_maxs_parallel(ws, dt, damped = True, damping = 1, stiffness = 100):

    x1maxs = np.zeros(len(ws))

    # use multiprocessing to speed up the calculation
    pool = mp.Pool(mp.cpu_count())
    results = [pool.apply_async(get_maxs, args=(w, dt, damped, damping, stiffness)) for w in ws]
    
    for i, result in enumerate(results):
        x1max = result.get()
        x1maxs[i] = x1max
    
    return x1maxs


if __name__ == '__main__':

    wn = np.sqrt(K1/M1)
    stiffness = m1 * wn**2

    ws = np.linspace(wn*0.1, wn*2, 100)

    dt = 0.0001
    
    x1maxs_undamped = get_maxs_parallel(ws, dt=dt, damped=False)
    x1maxs_damped_01 = get_maxs_parallel(ws, dt=dt, damped=True, damping=1e-3, stiffness=stiffness)
    x1maxs_damped_1 = get_maxs_parallel(ws, dt=dt, damped=True, damping=1e-2, stiffness=stiffness)
    x1maxs_damped_10 = get_maxs_parallel(ws, dt=dt, damped=True, damping=1e-1, stiffness=stiffness)

    #plt.plot(T, xinput, label='input')
    plt.plot(ws, x1maxs_undamped, label='undamped')
    plt.plot(ws, x1maxs_damped_01, label='damped 0.1')
    plt.plot(ws, x1maxs_damped_1, label='damped 1.0')
    plt.plot(ws, x1maxs_damped_10, label='damped 10.0')


    plt.legend()
    plt.show()
