import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

data52 = [ # W kg, T kg, xi -
    3, 1, 0.042435424,
    3, 2, 0.095823096,
    3, 3, 0.15,
    5, 1, 0.036199095,
    5, 2, 0.054973822,
    5, 3, 0.077452668
]

W, T, xi = np.array(data52).reshape(-1, 3).T

circumference = 3.4 / 12 # 12 v / (v / m) = m
eff_R = circumference / (2 * np.pi)
drum_R = 74 / 2 * 1e-3
g = 9.81
print(" effective tyre rolling radius R = ", 1e3*eff_R, "mm")

Llever = 27
Lweel = 15.8
droll = 12.4

X = T * g * drum_R / eff_R
Z = W * g * Llever / Lweel
#(735-465)/(900-735)

Z3 = Z[0]
Z5 = Z[3]

C22 = 244.3

def f3(xi, mu, offset=0):
    muZ = mu * Z3
    return muZ * (1 - muZ / (4 * C22 * xi)) + offset

def f5(xi, mu, offset=0):
    muZ = mu * Z5
    return muZ * (1 - muZ / (4 * C22 * xi)) + offset

popt3, _ = curve_fit(f3, xi[W == 3], X[W == 3], p0=[3, 10])
popt5, _ = curve_fit(f5, xi[W == 5], X[W == 5], p0=[3, 10])
mu3 = popt3[0]
mu5 = popt5[0]

# separate W into 5kg and 3kg

fig,ax = plt.subplots()

ax.plot(
    xi[W == 3], X[W == 3], 'o-', label=f'Z = {Z3:.1f} N'
)
x3 = np.linspace(*ax.get_xlim(), 100)
ax.plot(x3, f3(x3, *popt3), label=f'fit: $\mu = {mu3:.2f}$')

ax.plot(
    xi[W == 5], X[W == 5],'o-', label=f'Z = {Z5:.1f} N'
)
x5 = np.linspace(*ax.get_xlim(), 100)
ax.plot(x5, f5(x5, *popt5), label=f'fit: $\mu = {mu5:.2f}$')
# linear fit:
C11_3, intercept3 = np.polyfit(xi[W == 3], X[W == 3], 1)
C11_5, intercept5 = np.polyfit(xi[W == 5], X[W == 5], 1)

print("C11_3 = ", C11_3)
print("C11_5 = ", C11_5)

ax.set_xlabel(r'$ \xi$ (-)')
ax.set_ylabel('X (N)')
ax.grid()
ax.legend()

fig.savefig('IIB/4C8/52.png', dpi=300)
plt.show()



