import numpy as np
import matplotlib.pyplot as plt

data = [
-51.19,	0.50,
-31.57,	0.30,
-21.76,	0.20,
-12.57, 0.11,
-2.14, 0.02,
0.00, 0.00,
2.14, -0.05,
11.95,-0.19,
31.57,-0.29,
51.19,-0.45
]

force, voltage = np.array(data).reshape(-1, 2).T

# get correlation coefficient
r = np.corrcoef(voltage, force)[0, 1]

plt.plot(voltage, force, 'o-', label=f'r = {r:.3f}')
plt.xlabel('Voltage (V)')
plt.ylabel('Force (N)')
plt.grid()
plt.legend()
plt.savefig('IIB/4C8/Calibration/linearity.png', dpi=300)
plt.show()
