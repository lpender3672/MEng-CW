import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import multiprocessing as mp
from numba import jit, njit

#plt.rcParams["text.usetex"] = True
#plt.rcParams["font.family"] = "serif"

K1 = 1458.7 # strucutre stiffness
L1 = 1.98 # structure damping
M1 = 2.55

l1 = 0.1 # tuned mass damper damping
m1 = 0.05 # tuned mass damper mass
k1 = 28.6  # tuned mass damper stiffness

@jit(nopython=True)
def get_response(T, xinput, damped = True, stiffness = k1, damping = l1,  dt = 0.001):
    
    dxinput = np.zeros(len(xinput))
    dxinput[1:] = np.diff(xinput)/dt # input signal derivative

    x1 = 0 # initial conditions
    dx1 = 0 # initial conditions
    ddx1 = 0 # initial conditions

    y1 = 0 # initial conditions
    dy1 = 0# initial conditions
    ddy1 = 0 # initial conditions

    x1s = np.zeros(len(T))

    for i,t in enumerate(T):

        xin = xinput[i]
        dxin = dxinput[i]

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

    return x1s

def get_fft(w0, w1, damped, stiffness = k1, damping = l1):

    f0 = w0/(2*np.pi)
    f1 = w1/(2*np.pi)
    # create chirp signal
    fs = 10000
    dt = 1/fs
    T = np.arange(0, 100, dt) # time array
    xinput = sp.signal.chirp(T, f0=f0, f1=f1, t1=10, method='linear') # input signal
    dxinput = np.diff(xinput)/dt # input signal derivative

    response = get_response(T, xinput, damped, stiffness, damping, dt=dt)

    # get fft
    N = len(response)
    T = N/fs
    yf = np.abs(np.fft.fft(response) / N) ** 2
    #xf = np.arange(0, N)
    xf = np.arange(0, N) * 10 / np.argmax(yf)

    plt.plot(xf, yf, label=f'damping={damping}')


if __name__ == '__main__':

    wn = np.sqrt(K1/M1)
    stiffness = m1 * wn**2

    dt = 0.0001

    get_fft(wn*0.1, wn*2, damped = False)
    get_fft(wn*0.1, wn*2, damped = True, damping=l1, stiffness=stiffness)

    plt.xlim(7, 15)

    plt.legend()
    plt.show()
