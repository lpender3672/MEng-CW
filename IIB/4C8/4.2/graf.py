import matplotlib.pyplot as plt
import numpy as np

speed1_dat = np.loadtxt('IIB/4C8/4.2/4.2 - motor 1.csv', delimiter=',')
speed3_dat = np.loadtxt('IIB/4C8/4.2/4.2 - motor 3.csv', delimiter=',')
speed5_dat = np.loadtxt('IIB/4C8/4.2/4.2 - motor 5.csv', delimiter=',')
speed7_dat = np.loadtxt('IIB/4C8/4.2/4.2 - motor 7.csv', delimiter=',')

# zero all the data
speed1_dat[:, 0] -= speed1_dat[0, 0]
speed3_dat[:, 0] -= speed3_dat[0, 0]
speed5_dat[:, 0] -= speed5_dat[0, 0]
speed7_dat[:, 0] -= speed7_dat[0, 0]

xcal = 12 # V/m

slope = -104.935
intercept = -0.664

end = 0.73
start = 0.01

samples_to_reach_end1 = (speed1_dat / xcal)[(start < (speed1_dat / xcal)[:,0]) & ((speed1_dat / xcal)[:,0] < end), 0].shape[0]
samples_to_reach_end3 = (speed3_dat / xcal)[(start < (speed3_dat / xcal)[:,0]) & ((speed3_dat / xcal)[:,0] < end), 0].shape[0]
samples_to_reach_end5 = (speed5_dat / xcal)[(start < (speed5_dat / xcal)[:,0]) & ((speed5_dat / xcal)[:,0] < end), 0].shape[0]
samples_to_reach_end7 = (speed7_dat / xcal)[(start < (speed7_dat / xcal)[:,0]) & ((speed7_dat / xcal)[:,0] < end), 0].shape[0]

print(f'Speed 1: {samples_to_reach_end1} samples to reach end')
print(f'Speed 3: {samples_to_reach_end3} samples to reach end')
print(f'Speed 5: {samples_to_reach_end5} samples to reach end')
print(f'Speed 7: {samples_to_reach_end7} samples to reach end')

plt.plot(speed1_dat[:, 0]/ xcal, slope * speed1_dat[:, 1] + intercept, label='Speed 1')
plt.plot(speed3_dat[:, 0]/ xcal, slope * speed3_dat[:, 1] + intercept, label='Speed 3')
plt.plot(speed5_dat[:, 0]/ xcal, slope * speed5_dat[:, 1] + intercept, label='Speed 5')
plt.plot(speed7_dat[:, 0]/ xcal, slope * speed7_dat[:, 1] + intercept, label='Speed 7')

# print the avg force
f1 = slope * speed1_dat[:, 1] + intercept
f3 = slope * speed3_dat[:, 1] + intercept
f5 = slope * speed5_dat[:, 1] + intercept
f7 = slope * speed7_dat[:, 1] + intercept
d1 = speed1_dat[:, 0] / xcal
d3 = speed3_dat[:, 0] / xcal
d5 = speed5_dat[:, 0] / xcal
d7 = speed7_dat[:, 0] / xcal

print(f'Avg force for speed 1: {np.mean(f1[(start < d1) & (d1 < end)]):.2f} N')
print(f'Avg force for speed 3: {np.mean(f3[(start < d3) & (d3 < end)]):.2f} N')
print(f'Avg force for speed 5: {np.mean(f5[(start < d5) & (d5 < end)]):.2f} N')
print(f'Avg force for speed 7: {np.mean(f7[(start < d7) & (d7 < 0.4)]):.2f} N')

plt.xlabel('Distance (m)')
plt.ylabel('Lateral Force (N)')
plt.legend()
plt.grid()
plt.savefig('IIB/4C8/4.2/force_distances.png', dpi=300)
plt.show()