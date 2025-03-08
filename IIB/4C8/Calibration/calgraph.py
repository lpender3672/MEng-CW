import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


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

slope, intercept, r_value, p_value, std_err = stats.linregress(voltage, force)

# Degrees of freedom
n = len(voltage)
dof = n - 2

# Calculate t statistic for 95% confidence interval
t_crit = stats.t.ppf(1 - 0.025, dof)

# Confidence intervals
slope_ci = std_err * t_crit
intercept_se = std_err * np.sqrt(np.mean(voltage**2))
intercept_ci = intercept_se * t_crit

# Sampling
num_samples = 1000
sampled_slopes = np.random.uniform(slope - slope_ci, slope + slope_ci, num_samples)
sampled_intercepts = np.random.uniform(intercept - intercept_ci, intercept + intercept_ci, num_samples)

volt_range = np.linspace(voltage.min(), voltage.max(), 100)

upper_bound = np.full_like(volt_range, -np.inf)
lower_bound = np.full_like(volt_range, np.inf)

for m, c in zip(sampled_slopes, sampled_intercepts):
    fit = m * volt_range + c
    upper_bound = np.maximum(upper_bound, fit)
    lower_bound = np.minimum(lower_bound, fit)

print(f'Slope: {slope:.3f} ± {slope_ci:.3f}') 
print(f'Intercept: {intercept:.3f} ± {intercept_ci:.3f}')

# Plot data and fit
plt.plot(voltage, force, 'o', label='Data')
plt.plot(volt_range, intercept + slope * volt_range, 'r-', label='Linear fit')
plt.fill_between(volt_range, lower_bound, upper_bound, color='gray', alpha=0.3, label='95% CI')

plt.xlabel('Voltage (V)')
plt.ylabel('Force (N)')
plt.legend()
plt.grid()

plt.savefig('IIB/4C8/Calibration/linearity.png', dpi=300)
plt.show()

# Estimate error based on decimal precision

voltage_err = np.full_like(voltage, 0.005)

# Linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(voltage, force)

# Plot data with error bars
plt.errorbar(voltage, force, xerr=voltage_err, fmt='o', label='Data with Error Bars', ecolor='gray', capsize=3, markersize=1)

# Plot linear fit
volt_range = np.linspace(voltage.min(), voltage.max(), 100)
plt.plot(volt_range, intercept + slope * volt_range, 'r-', label='Linear fit')

plt.xlabel('Voltage (V)')
plt.ylabel('Force (N)')
plt.legend()
plt.grid()
plt.show()
