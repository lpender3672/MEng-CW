import numpy as np
import matplotlib.pyplot as plt




def radiative_forcing(C, C0=600):
    return 5.35 * np.log(C / C0)

def run_model(ECO2, time_final, additional_forcing = 0):

    heat_capacity = np.array([7.4e22, 5.3e24]) # J / K
    C_pre = 600 # Gt C
    tau = 276 # years
    k_carbon = 0.449

    E = 12/44 * ECO2 # E is in GtC / year

    dt = 0.01
    time = np.arange(0, time_final, dt)

    time_steps = len(time)

    C = np.zeros(time_steps)
    C[0] = 882 # Gt C

    T = np.zeros((time_steps, 2))
    T_base = 288
    T[:, 0] = 288 # upper ocean temperature
    T[:, 1] = 288 # lower oceam temperature

    lambda_sens = 1
    k_mix = 1
    Rearth = 6.371e6 #m

    Aearth = 4 * np.pi * Rearth**2

    forcing_array = np.zeros(time_steps)

    dt_s = dt * 60 * 60 * 24 * 365.25

    for t in range(1, time_steps):

        dC_dt = k_carbon * (E[t] - (C[t - 1] - C_pre) / tau) 
        C[t] = C[t - 1] + dC_dt * dt

        forcing = radiative_forcing(C[t]) + additional_forcing
        forcing_array[t] = forcing  # W/m^2

        CdT_dt = np.zeros(2)

        CdT_dt[0] = Aearth * (forcing - lambda_sens * (T[t - 1, 0] - T_base) - k_mix * (T[t - 1, 0] - T[t - 1, 1]))
        CdT_dt[1] = Aearth * (k_mix * (T[t - 1, 0] - T[t - 1, 1]))

        T[t] = T[t - 1] + CdT_dt * dt_s / heat_capacity

    return time, C, T

def plot_model(years = 25):

    E = np.zeros(years * 100)
    
    additional_forcing = 57.4e-3
    E[:25 * 100] = 37.4 * np.linspace(1, 0, 25 * 100) # Gt C / year for 100 years
    time, C, T = run_model(E, years, additional_forcing)

    fig, ax = plt.subplots(1, 2, figsize=(8, 4))

    ax[0].plot(time, T[:, 0]-273.15, label=f"Shallow ocean reservoir")
    ax[0].plot(time, T[:, 1]-273.15, label=f"Deep ocean reservoir")
    ax[0].legend()

    ax[0].set_xlabel("Time [years]")
    ax[0].set_ylabel("$T$ [K]")
    ax[0].grid()

    ax[1].plot(time, C/2.1)

    ax[1].set_xlabel("Time [years]")
    ax[1].set_ylabel("$CO_2$ Concentration [ppm]")
    ax[1].grid()

    fig.tight_layout()
    fig.savefig('IIB/4A7/contrail_avoidance/figures/model.png', dpi=300)

    return fig, ax


def methane_as_fuel_plot(fig, ax, years, additional_fuel = 0.01):
    LCV_kerosine = 43e6 # J/kg
    LCV_methane = 50e6#
    EI_H2O_kerosine = 1.29
    EI_H2O_methane = 2.25

    EI_CO2_methane = 2.75
    EI_CO2_kerosine = 3.15

    P = 26500 # 33000ft
    cp = 1001 # J/kgK at 33000 ft
    eta = 0.72
    epsilon = 0.622

    G_kerosine = P * EI_H2O_kerosine * cp / (epsilon * LCV_kerosine * (1-eta))
    G_methane = P * EI_H2O_methane * cp / (epsilon * LCV_methane * (1-eta))

    E = np.zeros(100 * years)

    base_forcing = 57.4e-3
    additional_forcing = base_forcing * G_methane / G_kerosine

    E[:] = 37.4 # Gt C / year for 100 years
    _, C_norm_methane, T_norm_methane = run_model(E, years, additional_forcing)

    E[:] = 37.4 + additional_fuel * 0.31 * EI_CO2_methane / EI_CO2_kerosine  # Gt C / year for 100 years
    time, C_avod_methane, T_avod_methane = run_model(E, years, 0)

    T = T_avod_methane - T_norm_methane
    F = radiative_forcing(C_avod_methane) - radiative_forcing(C_norm_methane) - additional_forcing

    AGWP = np.trapz(F[:] - F[0], time)
    AGTP = np.trapz(T[:, 0] - T[0,0], time)

    print(f"AGWP: {AGWP}")
    print(f"AGTP: {AGTP}")
    # plot

    #fig, ax = plt.subplots(1, 2, figsize=(8, 4))

    ax[0].plot(time, T[:, 0], label='Methane')
    
    ax[0].set_xlabel("Time [years]")
    ax[0].set_ylabel("$(T_{1,avd} - T_{1,dr})$ $[^oC]$")

    ax[1].plot(time, T[:, 1])
    ax[1].set_xlabel("Time [years]")
    ax[1].set_ylabel("$(T_{2,avd} - T_{2,dr})$ $[^oC]$")

    fig.tight_layout()
    #fig.savefig('IIB/4A7/contrail_avoidance/figures/methane.png', dpi=300)

    return fig, ax

def plot_basecase(fig, ax, years, additional_fuel = 0.01):

    E = np.zeros(years * 100)
    
    additional_forcing = 57.4e-3
    E[:] = 37.4 # Gt C / year for 100 years
    _, C_norm, T_norm = run_model(E, years, additional_forcing)

    E[:] = 37.4 + additional_fuel * 0.31  # Gt C / year for 100 years
    time, C_avod, T_avod = run_model(E, years, 0)

    T = T_avod - T_norm
    F = radiative_forcing(C_avod) - radiative_forcing(C_norm) - additional_forcing

    #fig, ax = plt.subplots(1, 2, figsize=(8, 4))

    ax[0].plot(time, T[:, 0], label="Baseline")

    ax[0].set_xlabel("Time [years]")
    ax[0].set_ylabel("$(T_{1,avd} - T_{1,dr})$ $[^oC]$")


    ax[1].plot(time, T[:, 1])

    ax[1].set_xlabel("Time [years]")
    ax[1].set_ylabel("$(T_{2,avd} - T_{2,dr})$ $[^oC]$")

    fig.tight_layout()
    #fig.savefig('IIB/4A7/contrail_avoidance/figures/baseline.png', dpi=300)

    return fig, ax

def higher_thermal_efficiency_plot(fig, ax, years, additional_fuel = 0.01):
    LCV_kerosine = 43e6 # J/kg
    EI_H2O_kerosine = 1.29

    P = 26500 # 33000ft
    cp = 1001 # J/kgK at 33000 ft
    eta_HI = 0.75
    eta_LO = 0.72
    epsilon = 0.622

    G_HI = P * EI_H2O_kerosine * cp / (epsilon * LCV_kerosine * (1-eta_HI))
    G_LO = P * EI_H2O_kerosine * cp / (epsilon * LCV_kerosine * (1-eta_LO))

    E = np.zeros(100 * years)

    print(G_HI / G_LO)

    base_forcing = 57.4e-3
    additional_forcing = base_forcing * G_HI / G_LO

    E[:] = 37.4 # Gt C / year for 100 years
    _, C_norm_eff, T_norm_eff = run_model(E, years, additional_forcing)

    E[:] = 37.4 + additional_fuel * 0.31  # Gt C / year for 100 years
    time, C_avod_eff, T_avod_eff = run_model(E, years, 0)

    T = T_avod_eff - T_norm_eff
    F = radiative_forcing(C_avod_eff) - radiative_forcing(C_norm_eff) - additional_forcing

    #fig, ax = plt.subplots(1, 2, figsize=(8, 4))

    ax[0].plot(time, T[:, 0], label='High $\eta$')
    
    ax[0].set_xlabel("Time [years]")
    ax[0].set_ylabel("$(T_{1,avd} - T_{1,dr})$ $[^oC]$")

    ax[1].plot(time, T[:, 1])
    ax[1].set_xlabel("Time [years]")
    ax[1].set_ylabel("$(T_{2,avd} - T_{2,dr})$ $[^oC]$")

    fig.tight_layout()
    #fig.savefig('IIB/4A7/contrail_avoidance/figures/methane.png', dpi=300)

    return fig, ax


fig, ax = plt.subplots(1, 2, figsize=(10, 4))

fig, ax = plot_basecase(fig, ax, 50, 0.01)
fig, ax = methane_as_fuel_plot(fig, ax, 50)
fig, ax = higher_thermal_efficiency_plot(fig, ax, 50)

ax[0].legend()
ax[0].grid()
ax[1].grid()

fig.savefig('IIB/4A7/contrail_avoidance/figures/avoidance_comparison.png', dpi=300)

plt.show()