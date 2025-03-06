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
eff_R = 1e3 * circumference / (2 * np.pi)
drum_R = 74 / 2 * 1e-3
g = 9.81
print(" effective tyre rolling radius R = ", eff_R, "mm")

X = T * g * eff_R / drum_R

Llever = 27
Lweel = 15.8
droll = 12.4

Z = W * g * 
#(735-465)/(900-735)

# separate W into 5kg and 3kg

plt.plot(
    X[W == 3], xi[W == 3], 'o-', label='W = 3kg'
)
plt.plot(
    X[W == 5], xi[W == 5], 'o-', label='W = 5kg'
)

plt.xlabel('T (kg)')
plt.ylabel('xi (-)')
plt.grid()
plt.legend()

plt.savefig('IIB/4C8/52.png', dpi=300)
plt.show()



