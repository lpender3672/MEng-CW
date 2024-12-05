import numpy as np
import matplotlib.pyplot as plt

def radiative_forcing(C, C0=600):
    return 5.35 * np.log(C / C0)

heat_capacity = np.array([1e21, 1e24]) # J / K
C_pre = 600 # Gt C
tau = 200 # years
k_carbon = 0.5

time_final = 10 # years
dt = 0.01
time = np.arange(0, time_final, dt)

time_steps = len(time)

E = np.zeros(time_steps)
E[100:200] = 2*37.4  # Gt C / year for 100 years

C = np.zeros(time_steps)
C[0] = C_pre

T = np.zeros((time_steps, 2))
T_base = 288
T[:, 0] = 288 # atmospheric temperature
T[:, 1] = 288 # ocean temperature

lambda_sens = 1
k_mix = 1
Rearth = 6.371e6 #m

Aearth = 4 * np.pi * Rearth**2

initial_forcing = radiative_forcing(C[0])
forcing_array = np.zeros(time_steps)

dt_s = dt * 60 * 60 * 24 * 365.25

for t in range(1, time_steps):

    dC_dt = k_carbon * (E[t] - (C[t - 1] - C_pre) / tau) 
    C[t] = C[t - 1] + dC_dt * dt

    forcing = radiative_forcing(C[t])
    forcing_array[t] = forcing # W/m^2

    CdT_dt = np.zeros(2)

    CdT_dt[0] = Aearth * (forcing - lambda_sens * (T[t - 1, 0] - T_base) - k_mix * (T[t - 1, 0] - T[t - 1, 1]))
    CdT_dt[1] = Aearth * (k_mix * (T[t - 1, 0] - T[t - 1, 1]))

    T[t] = T[t - 1] + CdT_dt * dt_s / heat_capacity


AGWP = np.trapz(forcing_array - initial_forcing, time)
AGTP = np.trapz(T[:, 0] - T_base, time)

print(f"AGWP: {AGWP}")
print(f"AGTP: {AGTP}")
# plot

fig, ax = plt.subplots(1, 1, figsize=(8, 4))

ax.plot(time, T[:, 0], label=f"Atmosphere reservoir")
ax.plot(time, T[:, 1], label=f"Ocean reservoir")

ax.set_xlabel("Time [years]")
ax.set_ylabel("Temperature [K]")

plt.legend()
plt.show()

fig, ax = plt.subplots(1, 1, figsize=(8, 4))

ax.plot(time, forcing_array, label="Carbon")

ax.set_xlabel("Time [years]")
ax.set_ylabel("Ft [W/m^2]")

plt.show()