import argparse
import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt


def MLKF_1dof(m1, l1, k1, f1):

    """Return mass, damping, stiffness & force matrices for 1DOF system"""

    M = np.array([[m1]])
    L = np.array([[l1]])
    K = np.array([[k1]])
    F = np.array([f1])

    return M, L, K, F


def MLKF_2dof(m1, l1, k1, f1, m2, l2, k2, f2):

    """Return mass, damping, stiffness & force matrices for 2DOF system"""

    M = np.array([[m1, 0], [0, m2]])
    L = np.array([[l1+l2, -l2], [-l2, l2]])
    K = np.array([[k1+k2, -k2], [-k2, k2]])
    F = np.array([f1, f2])

    return M, L, K, F


def freq_response(w_list, M, L, K, F):

    """Return complex frequency response of system"""

    return np.array(
        [np.linalg.solve(-w*w * M + 1j * w * L + K, F) for w in w_list]
    )


def time_response(t_list, M, L, K, F):

    """Return time response of system"""

    mm = M.diagonal()

    def slope(t, y):
        xv = y.reshape((2, -1))
        a = (F - L@xv[1] - K@xv[0]) / mm
        s = np.concatenate((xv[1], a))
        return s

    solution = scipy.integrate.solve_ivp(
        fun=slope,
        t_span=(t_list[0], t_list[-1]),
        y0=np.zeros(len(mm) * 2),
        method='Radau',
        t_eval=t_list
    )

    return solution.y[0:len(mm), :].T


def last_nonzero(arr, axis, invalid_val=-1):

    """Return index of last non-zero element of an array"""

    mask = (arr != 0)
    val = arr.shape[axis] - np.flip(mask, axis=axis).argmax(axis=axis) - 1
    return np.where(mask.any(axis=axis), val, invalid_val)


def plot(hz, sec, M, L, K, F):

    """Plot frequency and time domain responses"""

    # Generate response data

    f_response = np.abs(freq_response(hz * 2*np.pi, M, L, K, F))
    t_response = time_response(sec, M, L, K, F)

    # Determine suitable legends

    f_legends = (
        'm{} peak {:.4g} metre at {:.4g} Hz'.format(
            i+1,
            f_response[m][i],
            hz[m]
        )
        for i, m in enumerate(np.argmax(f_response, axis=0))
    )

    equilib = np.abs(freq_response([0], M, L, K, F))[0]         # Zero Hz
    toobig = abs(100 * (t_response - equilib) / equilib) >= 2
    lastbig = last_nonzero(toobig, axis=0, invalid_val=len(sec)-1)

    t_legends = (
        'm{} settled to 2% beyond {:.4g} sec'.format(
            i+1,
            sec[lastbig[i]]
        )
        for i, _ in enumerate(t_response.T)
    )

    # Create plot

    fig, ax = plt.subplots(2, 1, figsize=(11.0, 7.7))

    ax[0].set_title('Frequency domain response')
    ax[0].set_xlabel('Frequency/hertz')
    ax[0].set_ylabel('Amplitude/metre')
    ax[0].legend(ax[0].plot(hz, f_response), f_legends)

    ax[1].set_title('Time domain response')
    ax[1].set_xlabel('Time/second')
    ax[1].set_ylabel('Displacement/metre')
    ax[1].legend(ax[1].plot(sec, t_response), t_legends)

    fig.tight_layout()
    plt.show()


def main():

    """Main program"""

    # Parse arguments

    ap = argparse.ArgumentParser('Plot response curves')

    ap.add_argument('--m1', type=float, default=3.94, help='Mass 1 [3.94]')
    ap.add_argument('--l1', type=float, default=1.98, help='Damping 1 [1.98]')
    ap.add_argument('--k1', type=float, default=2100, help='Spring 1 [2100]')
    ap.add_argument('--f1', type=float, default=0.25, help='Force 1 [0.25]')

    ap.add_argument('--m2', type=float, help='Mass 2 [None]')
    ap.add_argument('--l2', type=float, default=0.5, help='Damping 2 [0.5]')
    ap.add_argument('--k2', type=float, default=53.4, help='Spring 2 [53.4]')
    ap.add_argument('--f2', type=float, default=0, help='Force 2 [0]')

    ap.add_argument(
        '--hz', type=float, nargs=2, default=(0, 5),
        help='Frequency range [0 5]'
    )
    ap.add_argument(
        '--sec', type=float, default=30,
        help='Time limit [30]'
    )

    args = ap.parse_args()

    # Generate matrices describing the system

    if args.m2 is None:
        M, L, K, F = MLKF_1dof(
            args.m1, args.l1, args.k1, args.f1
        )
    else:
        M, L, K, F = MLKF_2dof(
            args.m1, args.l1, args.k1, args.f1,
            args.m2, args.l2, args.k2, args.f2
        )

    # Generate frequency and time arrays

    hz = np.linspace(args.hz[0], args.hz[1], 10001)
    sec = np.linspace(0, args.sec, 10001)

    # Plot results

    plot(hz, sec, M, L, K, F)


if __name__ == '__main__':
    main()
