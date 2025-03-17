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

B = 10.0
C = 1.9
D = 1.0
E = 0.97

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

def magic_fit(xi, B, D):
    Fx = D * np.sin(
        C * np.arctan(
            B * xi - E * (B * xi - np.arctan(B * xi))
        )
    )
    return Fx

popt3, _ = curve_fit(f3, xi[W == 3], X[W == 3], p0=[3, 10])
popt5, _ = curve_fit(f5, xi[W == 5], X[W == 5], p0=[3, 10])
mu3 = popt3[0]
mu5 = popt5[0]

#mopt3, _ = curve_fit(magic_fit, xi[W == 3], X[W == 3], p0=[0, 1])
#mopt5, _ = curve_fit(magic_fit, xi[W == 5], X[W == 5], p0=[10, 1])

print("mu3 = ", mu3)
print("mu5 = ", mu5)

# separate W into 5kg and 3kg

fig,ax = plt.subplots()

ax.plot(
    xi[W == 3], X[W == 3], 'o-', label=f'Z = {Z3:.1f} N'
)
x3 = np.linspace(*ax.get_xlim(), 100)
muz = mu3 * Z3
fitlabel3 = f'$X = {muz:.1f}(1 - {muz:.1f}/(4C' + r'\xi)) ' + f'{popt3[1]:.1f}$'
ax.plot(x3, f3(x3, *popt3), label=fitlabel3)
#ax.plot(x3, magic_fit(x3, *mopt3), label="magic fit")

ax.plot(
    xi[W == 5], X[W == 5],'o-', label=f'Z = {Z5:.1f} N'
)
x5 = np.linspace(*ax.get_xlim(), 100)
muz = mu5 * Z5
fitlabel5 = f'$X = {muz:.1f}(1 - {muz:.1f}/(4C' + r'\xi)) +' + f'{popt5[1]:.1f}$' 
ax.plot(x5, f5(x5, *popt5), label=fitlabel5)
#ax.plot(x5, magic_fit(x5, *mopt5), label="magic fit")
# linear fit:
C11_3, intercept3 = np.polyfit(xi[W == 3], X[W == 3], 1)
C11_5, intercept5 = np.polyfit(xi[W == 5], X[W == 5], 1)

print(X[W == 3])

print("C11_3 = ", C11_3)
print("C11_5 = ", C11_5)

ax.set_xlabel(r'$ \xi$ (-)')
ax.set_ylabel('X (N)')
ax.grid()
ax.legend()

fig.savefig('IIB/4C8/52.png', dpi=300)


# --- Magic Formula parameters (example values) ---

# --- Define a range for the longitudinal creep factor xi ---
# (Adjust this range as needed for your application.)
xi = np.linspace(0, 0.15, 500)

# --- Magic Formula for longitudinal force (simplified) ---
#    F_x = D * sin( C * atan( B*xi - E*( B*xi - atan(B*xi ) ) ) )

Fx = magic_fit(xi, 10, 1)

fig ,ax =   plt.subplots()
# --- Plot longitudinal force vs. longitudinal creep factor ---
ax.plot(xi, Fx, label="F_x vs. xi")
ax.set_xlabel("Longitudinal creep factor, xi")
ax.set_ylabel("Longitudinal force F_x")
ax.set_title("Magic Formula: Longitudinal Force vs. Longitudinal Creep Factor")
ax.grid(True)
ax.legend()
plt.show()