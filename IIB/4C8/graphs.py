import numpy as np
import matplotlib.pyplot as plt


data52 = [ # W kg, T kg, xi -
    3, 1, 0.042435424,
    3, 2, 0.095823096,
    3, 3, 0.15,
    5, 1, 0.036199095,
    5, 2, 0.054973822,
    5, 3, 0.077452668
]

W, T, xi = np.array(data52).reshape(-1, 3).T

fig, ax = plt.subplots()

circumference = 3.4 / 12 # 12 v / (v / m) = m
eff_R = circumference / (2 * np.pi)
drum_R = 74 / 2 * 1e-3
g = 9.81
print(" effective tyre rolling radius R = ", 1e3*eff_R, "mm")

Llever = 27
Lweel = 15.8
droll = 12.4

X = T * g * eff_R / drum_R
Z = W * g * Llever / Lweel
#(735-465)/(900-735)

Z3 = Z[0]
Z5 = Z[3]

# separate W into 5kg and 3kg

plt.plot(
    xi[W == 3], X[W == 3], 'o-', label=f'Z = {Z3:.1f} N'
)
plt.plot(
    xi[W == 5], X[W == 5],'o-', label=f'Z = {Z5:.1f} N'
)
# linear fit:
C11_3, intercept3 = np.polyfit(xi[W == 3], X[W == 3], 1)
C11_5, intercept5 = np.polyfit(xi[W == 5], X[W == 5], 1)

print("C11_3 = ", C11_3)
print("C11_5 = ", C11_5)

plt.xlabel('xi (-)')
plt.ylabel('X (N)')
plt.grid()
plt.legend()

plt.savefig('IIB/4C8/52.png', dpi=300)
plt.show()



