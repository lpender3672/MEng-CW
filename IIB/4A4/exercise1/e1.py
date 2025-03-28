
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

def print_cg_fuel_table(cgA, smA, Afuel, cgB, smB, Bfuel):
    # Create a pandas DataFrame
    data = {
        "Fuel Mass (kg)": [Afuel, Bfuel],
        "Center of Gravity (CG)": [cgA, cgB],
        "System Mass (kg)": [smA, smB]
    }

    table = pd.DataFrame(data, index=["A", "B"])
    table = table.round({
        "Fuel Mass (kg)": 1,
        "Center of Gravity (CG)": 3,
        "System Mass (kg)": 1
    })

    print(table.to_latex(float_format="%.3f"))

def plot_Longitudinal_Static_Stability(ares, bres, aload, bload, afuel, bfuel):
    
    cgA, smA = calc_cg(aload, afuel)
    cgB, smB = calc_cg(bload, bfuel)

    #print_cg_fuel_table(cgA, smA, afuel, cgB, smB, bfuel)


    aCw = 2 * smA * g / (rho0 * (ares['Ve kt EAS'].to_numpy() * ms_per_kt) ** 2 * Sw )
    bCw = 2 * smB * g / (rho0 * (bres['Ve kt EAS'].to_numpy() * ms_per_kt) ** 2 * Sw )

    ares['Weight Coefficient -'] = aCw
    bres['Weight Coefficient -'] = bCw

    #print(ares.to_latex(float_format="%.3f"))
    #print(bres.to_latex(float_format="%.3f"))

    fig, ax = plt.subplots()
    aelev = ares['Elev deflection deg'].to_numpy()
    belev = bres['Elev deflection deg'].to_numpy()

    # insert 3.6 degrees at Cw = 0
    aCw = np.insert(aCw, 0, 0)
    aelev = np.insert(aelev, 0, 3.6)
    bCw = np.insert(bCw, 0, 0)
    belev = np.insert(belev, 0, 3.6)

    asrt = np.argsort(aCw)
    bsrt = np.argsort(bCw)

    ax.plot(aCw[asrt], aelev[asrt], "o-", label='A')
    ax.plot(bCw[bsrt], belev[bsrt], "o-", label='B')

    ax.set_xlabel(r'Weight coefficient $C_w$ [-]')
    ax.set_ylabel(r'Elevator angle $\eta$ [$^\circ$]')
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

    ax.set_xlabel(r'$x_{cg}/c$ [-]')
    ax.set_ylabel(r'$d\eta/dC_w$ [$^\circ$]')

    ax.legend()
    ax.grid()
    fig.tight_layout()
    fig.savefig(wdir / 'Longitudinal_Static_Stability_2.png', dpi=300)

    abeta = ares['Elev tab angle deg'].to_numpy()
    bbeta = bres['Elev tab angle deg'].to_numpy()

    # insert beta = -1.8 at Cw = 0
    abeta = np.insert(abeta, 0, -1.8)
    bbeta = np.insert(bbeta, 0, -1.8)

    fig, ax = plt.subplots()
    ax.plot(aCw[asrt], abeta[asrt], "o-", label='A')
    ax.plot(bCw[bsrt], bbeta[bsrt], "o-", label='B')

    ax.set_xlabel(r'Weight coefficient $C_w$ [-]')
    ax.set_ylabel(r'Trim tab deflection $\beta$ [$^\circ$]')
    ax.legend()

    ax.grid()
    fig.tight_layout()
    fig.savefig(wdir / 'Longitudinal_Static_Stability_3.png', dpi=300)

    A_dbeta_dCw = np.gradient(abeta[asrt], aCw[asrt])
    B_dbeta_dCw = np.gradient(bbeta[bsrt], bCw[bsrt])

    fig, ax = plt.subplots()

    Aymean = np.mean(A_dbeta_dCw)
    Bymean = np.mean(B_dbeta_dCw)

    ax.errorbar(cgA, Aymean, yerr=np.std(A_dbeta_dCw), fmt='o', label='A')
    ax.errorbar(cgB, Bymean, yerr=np.std(B_dbeta_dCw), fmt='o', label='B')

    x = np.linspace(20, 60, 100)
    y = Aymean + (x - cgA) * (Bymean - Aymean) / (cgB - cgA)
    ax.plot(x, y, label='Extrapolated', linestyle='--')

    # calc x at y = 0
    x0 = cgA - Aymean * (cgB - cgA) / (Bymean - Aymean)
    x0lab = '$x_{NP}/c = '+ f'{x0:.3f}' +'$'
    ax.vlines(x0, y.max(), y.min(), label= x0lab, linestyle='-', color='r')

    ax.set_xlabel(r'$x_{cg}/c$ [-]')
    ax.set_ylabel(r'$d\beta/dC_w$ [$^\circ$]')

    ax.legend()
    ax.grid()
    fig.tight_layout()
    fig.savefig(wdir / 'Longitudinal_Static_Stability_4.png', dpi=300)

def plot_Manoeuvre_Stability(ares, bres, aload, bload, afuel, bfuel):

    V = 180 * ms_per_kt

    cgA, smA = calc_cg(aload, afuel)
    cgB, smB = calc_cg(bload, bfuel)

    #print_cg_fuel_table(cgA, smA, afuel, cgB, smB, bfuel)

    a_nu = ares['Elev deflection deg'].to_numpy()
    b_nu = bres['Elev deflection deg'].to_numpy()
    a_nz = (ares['(n+1)g'].to_numpy() - 1 ) * 1
    b_nz = (bres['(n+1)g'].to_numpy() - 1 ) * 1

    ares['Normal acceleration g'] = a_nz
    bres['Normal acceleration g'] = b_nz


    #print(ares.to_latex(float_format="%.3f"))
    #print(bres.to_latex(float_format="%.3f"))

    # add point 0,0
    a_nz = np.insert(a_nz, 0, 0)
    a_nu = np.insert(a_nu, 0, 0)
    b_nz = np.insert(b_nz, 0, 0)
    b_nu = np.insert(b_nu, 0, 0)

    asrt = np.argsort(a_nz)
    bsrt = np.argsort(b_nz)

    fig, ax = plt.subplots()

    ax.plot(a_nz[asrt], a_nu[asrt], "o-", label='A')
    ax.plot(b_nz[bsrt], b_nu[bsrt], "o-", label='B')

    ax.set_xlabel(r'Normal acceleration $n_z$ [g]')
    ax.set_ylabel(r'Elevator deflection $\eta$ [$^\circ$]')

    ax.legend()
    ax.grid()
    fig.tight_layout()
    fig.savefig(wdir / 'Manoeuvre_Stability_1.png', dpi=300)

    A_dnu_dn = np.gradient(a_nu[asrt], a_nz[asrt])
    B_dnu_dn = np.gradient(b_nu[bsrt], b_nz[bsrt])

    fig, ax = plt.subplots()

    Aymean = np.mean(A_dnu_dn)
    Bymean = np.mean(B_dnu_dn)

    ax.errorbar(cgA, Aymean, yerr=np.std(A_dnu_dn), fmt='o', label='A')
    ax.errorbar(cgB, Bymean, yerr=np.std(B_dnu_dn), fmt='o', label='B')

    x = np.linspace(20, 100, 200)
    y = Aymean + (x - cgA) * (Bymean - Aymean) / (cgB - cgA)

    ax.plot(x, y, label='Extrapolated', linestyle='--')

    # calc x at y = 0
    x0 = cgA - Aymean * (cgB - cgA) / (Bymean - Aymean)
    x0lab = '$x_{MP}/c = '+ f'{x0:.3f}' +'$'
    ax.vlines(x0, y.max(), y.min(), label= x0lab, linestyle='-', color='r')

    ax.set_xlabel(r'$x_{cg}/c$ [-]')
    ax.set_ylabel(r'$d\eta/dn_z$ [$^\circ$]')
    ax.legend()
    ax.grid()
    fig.tight_layout()
    fig.savefig(wdir / 'Manoeuvre_Stability_2.png', dpi=300)

    a_f = ares['Stick force N'].to_numpy() #/ (0.5 * rho0 * V ** 2 * Sw)
    b_f = bres['Stick force N'].to_numpy() #/ (0.5 * rho0 * V ** 2 * Sw)

    fig, ax = plt.subplots()
    # f vs nz
    sasrt = asrt[1:] - 1
    sbsrt = bsrt[1:] - 1

    ax.plot(a_nz[asrt][1:], a_f[sasrt], "o-", label='A')
    ax.plot(b_nz[bsrt][1:], b_f[sbsrt], "o-", label='B')

    ax.set_xlabel(r'Normal acceleration $n_z$ [g]')
    ax.set_ylabel(r'Stick force $P_\eta$ [N]')

    ax.legend()
    ax.grid()
    fig.tight_layout()
    fig.savefig(wdir / 'Manoeuvre_Stability_3.png', dpi=300)

    A_df_dn = np.gradient(a_f[sasrt], a_nz[sasrt])
    B_df_dn = np.gradient(b_f[sbsrt], b_nz[sbsrt])

    fig, ax = plt.subplots()

    Aymean = np.mean(A_df_dn)
    Bymean = np.mean(B_df_dn)

    ax.errorbar(cgA, Aymean, yerr=np.std(A_df_dn), fmt='o', label='A')
    ax.errorbar(cgB, Bymean, yerr=np.std(B_df_dn), fmt='o', label='B')

    x = np.linspace(20, 260, 200)
    y = Aymean + (x - cgA) * (Bymean - Aymean) / (cgB - cgA)

    ax.plot(x, y, label='Extrapolated', linestyle='--')

    # calc x at y = 0
    x0 = cgA - Aymean * (cgB - cgA) / (Bymean - Aymean)
    x0lab = '$x_{MP}/c = '+ f'{x0:.3f}' +'$'
    ax.vlines(x0, y.max(), y.min(), label= x0lab, linestyle='-', color='r')

    ax.set_xlabel(r'$x_{cg}/c$ [-]')
    ax.set_ylabel(r'$dP_\eta/dn_z$ [N/g]')
    ax.legend()
    ax.grid()
    fig.tight_layout()
    fig.savefig(wdir / 'Manoeuvre_Stability_4.png', dpi=300)

def plot_Lat_Directional_Static_Stability_SHSS(ares, bres, aload, bload):

    print(ares.to_latex(float_format="%.3f"))
    print(bres.to_latex(float_format="%.3f"))

    fig, ax = plt.subplots()
    a_roll = ares['Roll angle deg'].to_numpy().astype(float)
    b_roll = bres['Roll angle deg'].to_numpy().astype(float)
    a_sideslip = ares['Sideslip deg'].to_numpy().astype(float)
    b_sideslip = bres['Sideslip deg'].to_numpy().astype(float)

    # roll vs sideslip
    asrt = np.argsort(a_sideslip)
    bsrt = np.argsort(b_sideslip)

    ax.plot(a_sideslip[asrt], a_roll[asrt], "o", label='Group A Standard')
    ax.plot(b_sideslip[bsrt], b_roll[bsrt], "o", label='Group B Flaps $20^\circ$ and Landing Gear Down')

    corrective_fit1 = np.polyfit(a_sideslip[asrt], a_roll[asrt], 1)
    corrective_fit2 = np.polyfit(b_sideslip[bsrt], b_roll[bsrt], 1)
    ax.plot(a_sideslip[asrt], np.polyval(corrective_fit1, a_sideslip[asrt]), 'r--', label='Group A fit')
    ax.plot(b_sideslip[bsrt], np.polyval(corrective_fit2, b_sideslip[bsrt]), 'g--', label='Group B fit')

    ax.set_xlabel(r'Sideslip angle $\beta$ [$^\circ$]')
    ax.set_ylabel(r'Angle of bank $\phi$ [$^\circ$]')

    ax.legend()
    ax.grid()
    fig.tight_layout()
    fig.savefig(wdir / 'Lat_Directional_Static_Stability_SHSS_1.png', dpi=300)

    # plot rudder and aerilon angle against sideslip
    fig, ax = plt.subplots()
    a_aileron = ares['Aileron deg'].to_numpy().astype(float)
    b_aileron = bres['Aileron deg'].to_numpy().astype(float)

    a_rudder = ares['Rudder deg'].to_numpy().astype(float)
    b_rudder = bres['Rudder deg'].to_numpy().astype(float)

    ax.plot(a_sideslip[asrt], a_aileron[asrt], "o", label='Group A Standard')
    ax.plot(b_sideslip[bsrt], b_aileron[bsrt], "o", label='Group B Flaps $20^\circ$ and Landing Gear Down')

    corrective_fit3 = np.polyfit(a_sideslip[asrt], a_aileron[asrt], 1)
    corrective_fit4 = np.polyfit(b_sideslip[bsrt], b_aileron[bsrt], 1)
    ax.plot(a_sideslip[asrt], np.polyval(corrective_fit3, a_sideslip[asrt]), 'r--', label='Group A fit')
    ax.plot(b_sideslip[bsrt], np.polyval(corrective_fit4, b_sideslip[bsrt]), 'g--', label='Group B fit')

    ax.set_xlabel(r' Sideslip angle $\beta$ [$^\circ$]')
    ax.set_ylabel(r' Aileron deflection $\delta_{ail}$ [$^\circ$]')

    ax.legend()
    ax.grid()

    fig.tight_layout()
    fig.savefig(wdir / 'Lat_Directional_Static_Stability_SHSS_2.png', dpi=300)

    fig, ax = plt.subplots()
    ax.plot(a_sideslip[asrt], a_rudder[asrt], "o", label='Group A Standard')
    ax.plot(b_sideslip[bsrt], b_rudder[bsrt], "o", label='Group B Flaps $20^\circ$ and Landing Gear Down')

    corrective_fit5 = np.polyfit(a_sideslip[asrt], a_rudder[asrt], 1)
    corrective_fit6 = np.polyfit(b_sideslip[bsrt], b_rudder[bsrt], 1)
    ax.plot(a_sideslip[asrt], np.polyval(corrective_fit5, a_sideslip[asrt]), 'r--', label='Group A fit')
    ax.plot(b_sideslip[bsrt], np.polyval(corrective_fit6, b_sideslip[bsrt]), 'g--', label='Group B fit')
    
    ax.set_xlabel(r' Sideslip angle $\beta$ [$^\circ$]')
    ax.set_ylabel(r' Rudder deflection $\delta_{rud}$ [$^\circ$]')

    ax.legend()
    ax.grid()
    fig.tight_layout()
    fig.savefig(wdir / 'Lat_Directional_Static_Stability_SHSS_3.png', dpi=300)


def main():
        
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

    """
    plot_Longitudinal_Static_Stability(
        A_Longitudinal_Static_Stability_df, 
        B_Longitudinal_Static_Stability_df, 
        loadA, loadB, 
        A_Longitudinal_Static_Stability_fuel, 
        B_Longitudinal_Static_Stability_fuel
        )
    """

    plot_Manoeuvre_Stability(
        A_Longitudinal_Manoeuvre_Stability_df, 
        B_Longitudinal_Manoeuvre_Stability_df, 
        loadA, loadB, 
        A_Longitudinal_Manoeuvre_Stability_fuel, 
        B_Longitudinal_Manoeuvre_Stability_fuel
        )
    
    """
    plot_Lat_Directional_Static_Stability_SHSS(
        A_Lat_Directional_Static_Stability_SHSS_df, 
        B_Lat_Directional_Static_Stability_SHSS_df, 
        loadA, loadB
        )
    """


    plt.show()

if __name__ == "__main__":
    main()
