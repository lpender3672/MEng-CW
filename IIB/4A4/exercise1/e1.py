
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# import lib to open xlsx files
import openpyxl
import os
from pathlib import Path

plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams['font.size'] = 12

wdir = Path(os.getcwd()) / 'IIB/4A4/exercise1'
wbpath = wdir / 'exercise1data_2024.xlsx'

load_df = pd.read_excel(wbpath, sheet_name='Loadings', skiprows=6, header=None)
measurement_df = pd.read_excel(wbpath, sheet_name='Measurements')

loadA = load_df.iloc[:-1, [0, 1, 2, 3, 10]].replace(np.nan, 0)
loadB = load_df.iloc[:-1, [0, 6, 7, 8, 10]].replace(np.nan, 0)

ballast = load_df.iloc[-1, 0]

# consts
global g, rho0, P0, T0, Sw, c, ms_per_kt, m_per_ft
g = 9.81 # m/s^2
rho0 = 1.225 # kg/m^3
P0 = 101325 # Pa
T0 = 288.15 # K
Sw = 41.8 # m^2 gross wing area
c = 2.08 # m mean chord
ms_per_kt = 0.51444
m_per_ft = 0.3048

# mass and positions
global demon_mass, demon_pos, crewed_saab340B_mass, crewed_saab340B_pos, ballast_mass, ballast_pos, fuel_pos
demon_mass = 80
demon_pos = 6.91
crewed_saab340B_mass = 8695
crewed_saab340B_pos = 10.69
ballast_mass = 200
ballast_pos = 17.12
fuel_pos = 11.18


def calc_cg(load_df, fuel_mass = 0):

    smx = (
        demon_mass * demon_pos +
        crewed_saab340B_mass * crewed_saab340B_pos +
        ballast_mass * ballast_pos +
        fuel_mass * fuel_pos
    )
    sm = demon_mass + crewed_saab340B_mass + ballast_mass + fuel_mass

    mx = load_df.iloc[:, 1:4].sum(axis=1)
    smx += (mx * load_df.iloc[:, 4]).sum()
    sm += load_df.iloc[:, 1:4].sum().sum()

    cg = (smx / sm - 10.472) * 100 / 2.085

    return cg, sm

def plot_Longitudinal_Static_Stability(ares, bres, aload, bload, afuel, bfuel):
    
    cgA, smA = calc_cg(aload, afuel)
    cgB, smB = calc_cg(bload, bfuel)

    aCw = 2 * smA * g / (rho0 * (ares['Ve kt EAS'].to_numpy() * ms_per_kt) ** 2 * Sw )
    bCw = 2 * smB * g / (rho0 * (bres['Ve kt EAS'].to_numpy() * ms_per_kt) ** 2 * Sw )

    fig, ax = plt.subplots()
    aelev = ares['Elev deflection deg'].to_numpy()
    belev = bres['Elev deflection deg'].to_numpy()

    asrt = np.argsort(aCw)
    bsrt = np.argsort(bCw)

    ax.plot(aCw[asrt], aelev[asrt], label='A')
    ax.plot(bCw[bsrt], belev[bsrt], label='B')

    ax.set_xlabel('$C_w$')
    ax.set_ylabel('$\eta$ [$^\circ$]')
    ax.legend()

    ax.grid()
    fig.tight_layout()
    fig.savefig(wdir / 'Longitudinal_Static_Stability_1.png', dpi=300)

    A_delev_dCw = np.gradient(aelev[asrt], aCw[asrt])
    B_delev_dCw = np.gradient(belev[bsrt], bCw[bsrt])

    fig, ax = plt.subplots()

    Aymean = np.mean(A_delev_dCw)
    Bymean = np.mean(B_delev_dCw)

    ax.errorbar(cgA, Aymean, yerr=np.std(A_delev_dCw), fmt='o', label='A')
    ax.errorbar(cgB, Bymean, yerr=np.std(B_delev_dCw), fmt='o', label='B')

    x = np.linspace(20, 52, 100)
    y = Aymean + (x - cgA) * (Bymean - Aymean) / (cgB - cgA)
    ax.plot(x, y, label='Extrapolated', linestyle='--')

    # calc x at y = 0
    x0 = cgA - Aymean * (cgB - cgA) / (Bymean - Aymean)
    x0lab = '$x_{NP}/c = '+ f'{x0:.3f}' +'$'
    ax.vlines(x0, y.max(), y.min(), label= x0lab, linestyle='-', color='r')

    ax.set_xlabel('$x_{cg}/c$')
    ax.set_ylabel('$d\eta/dC_w$')

    ax.legend()
    ax.grid()
    fig.tight_layout()
    fig.savefig(wdir / 'Longitudinal_Static_Stability_2.png', dpi=300)


A_Longitudinal_Static_Stability_df = measurement_df.iloc[5:10, 0:3]
A_Longitudinal_Static_Stability_fuel = measurement_df.iloc[10, 3]
A_Longitudinal_Static_Stability_df.columns = ['Ve kt EAS', 'Elev deflection deg', 'Elev tab angle deg']
A_Longitudinal_Manoeuvre_Stability_df = measurement_df.iloc[18:23, 0:3]
A_Longitudinal_Manoeuvre_Stability_fuel = measurement_df.iloc[23, 3]
A_Longitudinal_Manoeuvre_Stability_df.columns = ['Elev deflection deg', 'Stick force N', '(n+1)g']
A_Lat_Directional_Static_Stability_SHSS_df = measurement_df.iloc[30:37, 0:4]
A_Lat_Directional_Static_Stability_SHSS_df.columns = ['Aileron deg', 'Roll angle deg', 'Sideslip deg', 'Rudder deg']

B_Longitudinal_Static_Stability_df = measurement_df.iloc[5:10, 8:11]
B_Longitudinal_Static_Stability_fuel = measurement_df.iloc[10, 11]
B_Longitudinal_Static_Stability_df.columns = ['Ve kt EAS', 'Elev deflection deg', 'Elev tab angle deg']
B_Longitudinal_Manoeuvre_Stability_df = measurement_df.iloc[18:23, 8:11]
B_Longitudinal_Manoeuvre_Stability_fuel = measurement_df.iloc[23, 11]
B_Longitudinal_Manoeuvre_Stability_df.columns = ['Elev deflection deg', 'Stick force N', '(n+1)g']
B_Lat_Directional_Static_Stability_SHSS_df = measurement_df.iloc[30:37, 8:12]
B_Lat_Directional_Static_Stability_SHSS_df.columns = ['Aileron deg', 'Roll angle deg', 'Sideslip deg', 'Rudder deg']


plot_Longitudinal_Static_Stability(
    A_Longitudinal_Static_Stability_df, 
    B_Longitudinal_Static_Stability_df, 
    loadA, loadB, 
    A_Longitudinal_Static_Stability_fuel, 
    B_Longitudinal_Static_Stability_fuel)

plt.show()
