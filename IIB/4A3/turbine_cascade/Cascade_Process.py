#   Cascade_Process                              
#                               
#   Script to process data from 4A3 turbine cascade experiment
#
#   Written by James Taylor                
#   August 2022
#
#   Instructions:
#       Get numpy, matplotlib and mat73 packages 
#       Change the filename and directory to point to your data
#       Put cascade.mat file in the same place
#       Execute the python script
#       Use data printed to screen and saved plots for your report
#
#   All data is loaded or stored in dictionaries:
#       b - Cascade geometrical parameters, CFD and previous data
#       e - Your experimental data logged on the cascade
#       N - Channel numbers from the experiment
#       t - Processed wake traverse data
#       s - Processed surface pressure data

# Import modules
import numpy as np
import matplotlib.pyplot as plt 
import mat73
import scipy.interpolate as interp
from matplotlib.patches import FancyArrow

plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams['figure.facecolor'] = 'white'

def general(e,N):
    # Use first point from the traverse for approximate calculations

    # Index historical data to select first traverse point
    q = e['t'] == e['t_wake'][0]

    # Atmospheric pressure at exit
    Pa = e['Pa'][q]

    # Average inlet static pressure
    P_in = np.mean(e['P_wake'][0,N['dsa']['P_1']]) + Pa
    
    # Inlet total pressure
    Po_in = e['P_wake'][0,N['dsa']['Po_1']] + Pa

    # Density using inlet stagnation conditions
    ro = Po_in / (e['R'][q] * e['T'][q])
    
    # Print quantities to screen
    print('\n\n1 - General\n\nFirst traverse point approximate data')
    print('Poin = %4.1f KPa , Pin = %4.1f KPa , Pa = %4.1f KPa , ro = %3.2f kg/m3\n\n' 
        % (Po_in/1000,P_in/1000,Pa/1000,ro))


def exit_traverse(e,N,b):
    # Use probe data from exit wake traverse for detailed calculations

    # Initialise dictionaries for processed data and plots
    t = {}; h = {};

    # Open figure window for all wake plots
    h['wake'],ax = plt.subplots(nrows=4, ncols=1, figsize=(5,10),
        sharex='col',num='Exit Traverse')
    cols = gen_cols()

    # Set axes names and formating for subplots
    ynames = ['($P_{01} - P_{02}$) / ($P_{01} - P_{2,av}$)',
              '($P_{1} - P_{2}$) / ($P_{01} - P_{2,av}$)',
              '$V_2$ / $V_{2,s}$',r'$\alpha_2 / ^\circ$']
    for n in range(3):
        plt.setp(ax[n].get_xticklabels(), visible=False)
        set_axes(ax[n],'',ynames[n])
    set_axes(ax[3],'y / s',ynames[3])

    # Figure window for yaw calibration
    h['yaw'] = plt.figure('Yaw Calibration'); ax_yaw = plt.gca();
    set_axes(ax_yaw,r'$\alpha_{probe} / ^\circ$','$C_{yaw}$')

    # Stagnation pressure loss coefficient
    Po_2 = e['P_wake'][:,N['probe']['Po']]
    Po_1 = e['P_wake'][:,N['dsa']['Po_1']]
    P_2_av = 0
    t['Yp'] = (Po_1 - Po_2) / (Po_1 - P_2_av) 

    # Static pressure coefficient
    P_1 = np.mean(e['P_wake'][:,N['dsa']['P_1']],axis=1)
    P_2 = e['P_wake'][:,N['probe']['P']]
    t['Cp'] = (P_1 - P_2) / (Po_1 - P_2_av)

    # Velocity ratio
    t['V2_V2s'] = ((Po_2 - P_2) / (Po_1 - P_2))**0.5
    t['V2_V2s_av'] = np.trapz(t['V2_V2s'],x=e['y_wake']) / b['s']

    # Calculate non-dimensional pitch
    t['y_s'] = e['y_wake'] / b['s'] 

    #plt.plot(t['y_s'], P_2)
    #plt.show()
    #exit()

    # Yaw coefficient from probe side holes
    P_l = e['P_ang'][:,N['probe']['P_l']]
    P_r = e['P_ang'][:,N['probe']['P_r']]
    Po = e['P_ang'][:,N['probe']['Po']]
    P = e['P_ang'][:,N['probe']['P']]
    Cyaw_cal = (P_l - P_r) / (Po - P)
    inc_cal = e['theta'][1] - e['theta']

    # Interpolate probe incidence angle from calibration curve
    f = interp.interp1d(Cyaw_cal,inc_cal,kind='linear',fill_value='extrapolate')
    P_l = e['P_wake'][:,N['probe']['P_l']]
    P_r = e['P_wake'][:,N['probe']['P_r']]
    Cyaw = (P_l - P_r) / (Po_2 - P_2)
    inc = f(Cyaw)

    # Calculate yaw angle from probe incidence
    t['alpha_2'] = e['theta'][1] + inc

    # Plot yaw calibration and actual traverse values
    ax_yaw.plot(inc_cal,Cyaw_cal,'o-',color=cols[1,:],label='Angle calibration')
    ax_yaw.plot(inc,Cyaw,'.',color=cols[0,:],label='Traverse points')
    ax_yaw.legend()

    # Plot the flow across the pitch of the passage
    ax[0].plot(t['y_s'],t['Yp'],'.-',color=cols[0,:])
    ax[1].plot(t['y_s'],t['Cp'],'.-',color=cols[0,:])
    ax[2].plot(t['y_s'],t['V2_V2s'],'.-',color=cols[0,:])
    ax[3].plot(t['y_s'],t['alpha_2'],'.-',color=cols[0,:])

    # Density using outlet static conditions
    q = np.in1d(e['t'],e['t_wake'])
    t['R'] = e['R'][q]; t['T'] = e['T'][q]; t['ga'] = e['ga'][q];
    t['ro'] = e['Pa'][q] / (t['R'] * t['T'])

    # Mass average loss coefficient, incompressible so density cancels
    t['V_2'] = ((Po_2 - P_2) / (0.5 * t['ro']))**0.5
    Vx_2 = t['V_2'] * np.cos(np.deg2rad(t['alpha_2']))
    t['Yp_av'] = np.trapz(Vx_2 * t['Yp'],x=e['y_wake']) / np.trapz(Vx_2,x=e['y_wake'])

    # Axial force per unit span from momentum change and pressure difference
    V_1 = ((Po_1 - P_1) / (0.5 * t['ro']))**0.5
    t['Fx,m,1'] = np.trapz(t['ro'] * V_1**2,x=e['y_wake'])
    t['Fx,m,2'] = np.trapz(t['ro'] * Vx_2**2,x=e['y_wake'])
    t['Fx,p,1'] = np.trapz(P_1,x=e['y_wake'])
    t['Fx,p,2'] = np.trapz(P_2,x=e['y_wake'])
    
    # Tangential force per unit span from momentum change in y-direction
    Vy_2 = t['V_2'] * np.sin(np.deg2rad(t['alpha_2']))
    t['Fy,m,2'] = np.trapz(t['ro'] * Vx_2 * Vy_2,x=e['y_wake'])

    # Average flow angle from momentum ratios
    t['alpha_2_av'] = np.rad2deg(np.arctan2(t['Fy,m,2'],t['Fx,m,2']))

    # Axial velocity ratio
    t['AVR'] = np.trapz(t['ro'] * Vx_2,x=e['y_wake']) / np.trapz(t['ro'] * V_1,x=e['y_wake'])
    t['AVR_hd'] = np.trapz(Vx_2 / V_1,x=e['y_wake']) / b['s']

    print(f"AVR calculated using equation in handout:", t['AVR_hd'])

    # Plot averaged quantities
    ax[0].plot(np.array([0,1]),np.ones(2) * t['Yp_av'],'-',color=cols[2,:])
    ax[2].plot(np.array([0,1]),np.ones(2) * t['V2_V2s_av'],'-',color=cols[2,:])
    ax[3].plot(np.array([0,1]),np.ones(2) * t['alpha_2_av'],'-',color=cols[2,:])

    # Print quantities to screen
    print('2 - Exit Traverse\n\nProcessed and averaged data from probe & tunnel')
    print('Yp,av = %5.4f , Alpha,2,av = %4.2f , AVR = %4.3f' 
        % (t['Yp_av'],t['alpha_2_av'],t['AVR']))
    print('Fx,m,1 = %4.1f , Fx,m,2 = %4.1f , Fx,p,1 = %4.1f , Fx,p,2 = %4.1f' 
        % (t['Fx,m,1'],t['Fx,m,2'],t['Fx,p,1'],t['Fx,p,2']))
    print('Fy,m,1 = %4.1f , Fy,m,2 = %4.1f\n\n' 
        % (0.0,t['Fy,m,2']))
    
    # create new plot
    h['quiver'], axq = plt.subplots(nrows=1, ncols=2, figsize=(12,6),num='Exit Quiver');
    gs = h['quiver'].add_gridspec(1, 2, width_ratios=[1, 2])

    # Plot the blade geometry
    xys = np.array(e['xy_ps'])
    maxy = np.max(xys[:,1])
    
    axq[0] = plot_cascade(axq[0], e)
    axq[1] = plot_cascade(axq[1], e)
    
    #axq.axis('equal')
    # plot quiver plot of velocity vectors
    Cx = 30.323
    top = Cx * maxy
    yvals = reduce_dataset(e['y_wake'])

    vs = reduce_dataset(t['V_2'])
    alphas = reduce_dataset(t['alpha_2'])

    vs_scaled = vs - 0.9 * np.min(vs)
    vxs_scaled = vs_scaled * np.cos(np.deg2rad(alphas))
    vys_scaled = vs_scaled * np.sin(np.deg2rad(alphas))
    dalpha = alphas - 71.24

    xq = Cx * np.ones(yvals.shape)
    q1 = axq[0].quiver(xq, top + yvals - 15, vxs_scaled, vys_scaled, dalpha, angles='xy', scale_units='xy', scale=1, cmap = 'jet')
    q2 = axq[1].quiver(xq, top + yvals - 15, vxs_scaled, vys_scaled, dalpha, angles='xy', scale_units='xy', scale=1, cmap = 'jet', label='Scaled, Offset Velocity Vectors')
    # add colourbar with velocity scale with label
    h['quiver'].colorbar(q2, label=r'$\alpha - 71.24$ / $^\circ$')

    # plot lines at 71.24 degrees at several heights
    heights = yvals
    for height in heights:
        x = np.array([0, 100])
        y = np.tan(np.deg2rad(71.24)) * x + top + height - 15
        axq[1].plot(Cx + x, y, 'k--', linewidth=0.5, alpha=0.5)


    axq[0].set_xlim([-20, Cx + 20])
    axq[0].set_aspect('equal')

    # set ylim
    xbounds = [Cx - 5, Cx + 5]
    ybounds = [top - 20, top + 30]

    axq[1].set_xlim(xbounds)
    axq[1].set_ylim(ybounds)
    # draw rectangle on axq[0] shoinw the region of axq[1]
    rect = plt.Rectangle((xbounds[0], ybounds[0]), xbounds[1] - xbounds[0], ybounds[1] - ybounds[0], edgecolor='g', facecolor='none', label='Right Plot Region')
    axq[0].add_patch(rect)

    axq[0].set_xlabel('x / mm')
    axq[0].set_ylabel('y / mm')
    axq[1].set_xlabel('x / mm')
    axq[1].set_ylabel('y / mm')
    

    h['quiver'].tight_layout()
    # add legend
    axq[0].legend()
    axq[1].legend(loc='upper left')

    return(t,h)

def reduce_dataset(arr):
    n = arr.shape[0]

    first4 = arr[0:3]
    middle_sample = arr[4:n-4:4]
    last4 = arr[n-4:n]

    return np.concatenate((first4, middle_sample, last4))

def plot_cascade(ax, e):
    # Plot the cascade geometry

    pos = [0,0]
    ax = plot_blade(ax,e, pos)
    pos = [0,-30]
    ax = plot_blade(ax,e, pos)
    pos = [0,30]
    ax = plot_blade(ax,e, pos)

    ax = plot_surfaces(ax, e, [0,0])

    ax = plot_control_volume(ax, e, [0,0])

    return ax

def plot_surfaces(ax, e, pos):
    Cx = 30.323 # mm
    # Plot the suction surface
    
    xyp =  pos + Cx * np.array(e['xy_ps'])
    xys = pos + Cx * np.array(e['xy_ss'])
    # append the last pressure surface point to the suction surface
    xys = np.append(xys, [xyp[-1,:]], axis=0)
    xyp[:,1] = xyp[:,1] - 30
    # concate the two arrays but reverse the second one
    # offset all points by pos

    # plot the blade as closed plot
    ax.plot(xys[:,0],xys[:,1],'b-', label='Suction Surface')
    ax.plot(xyp[:,0],xyp[:,1],'r-', label='Pressure Surface')

    return(ax)

def plot_control_volume(ax, e, pos):
    Cx = 30.323 # mm

    xyp =  pos + Cx * np.array(e['xy_ps'])
    xys = pos + Cx * np.array(e['xy_ss'])

    xys = np.append(xys, [xyp[-1,:]], axis=0)

    xs = xys[:,0]
    ys = xys[:,1]
    xp = xyp[:,0]
    yp = xyp[:,1]

    fs = interp.interp1d(xs, ys, kind='linear', fill_value='extrapolate')
    fp = interp.interp1d(xp, yp, kind='linear', fill_value='extrapolate')
    xlin = np.linspace(-2, Cx, 100)
    ysuc = fs(xlin)
    ypres = fp(xlin)
    ycenter = (ysuc + ypres) / 2

    y_cv_upper = ycenter + 15
    y_cv_lower = ycenter - 15

    # plot the control volume
    ax.plot(xlin, y_cv_upper, 'k--', linewidth=1, alpha=1, label='Control Volume')
    ax.plot([xlin[0],xlin[0]], [y_cv_upper[0], y_cv_lower[0]], 'k--', linewidth=1, alpha=1)
    ax.plot(xlin, y_cv_lower, 'k--', linewidth=1, alpha=1)
    ax.plot([xlin[-1], xlin[-1]], [y_cv_upper[-1], y_cv_lower[-1]], 'k--', linewidth=1, alpha=1)


    return ax



def lift_distribution(e,N,t,b):
    # Use manometer data for detailed calculations on pressure distribution

    # Initialise dictionary for processed data
    s = {}

    # Figure window for lift distribution
    h = plt.figure('Velocity Distribution'); ax = plt.gca();
    set_axes(ax,'x / Cx','$V_s / V_{2,s}$')
    cols = gen_cols()

    # Plot the CFD velocity distribution
    b['Vs_V2s'] = b['v'] * np.cos(np.deg2rad(b['alpha_2']))
    b['x_cx'] = (b['x'] - np.min(b['x'])) / (np.max(b['x']) - np.min(b['x'])) 
    ax.plot(b['x_cx'],b['Vs_V2s'],'-',color=cols[1,:],label='Inviscid Solution')

    # Concatenate the SS and PS measurements in a single complete loop
    iss = N['h2o']['Pss']; ips = N['h2o']['Pps'];
    leng = e['xy_ss'].shape[0]
    P = np.concatenate((e['P_h2o'][iss],np.flip(e['P_h2o'][ips]),
        np.expand_dims(e['P_h2o'][iss][0],axis=0)))

    # Join coordinates from both sides together
    s['xy'] = np.concatenate((e['xy_ss'],np.flip(e['xy_ps'],axis=0),
        np.expand_dims(e['xy_ss'][0],axis=0)))

    # Blade surface pressure coefficients
    Po_1 = e['P_h2o'][N['h2o']['Po_1']]; P_2 = 0;
    s['Cp'] = (Po_1 - P) / (Po_1 - P_2)

    # Isentropic velocity ratio
    s['Vs_V2s'] = s['Cp']**0.5

    # this is absolutely grim but not much worse than james' cryptic dictionary keys
    arr = np.array(s['Vs_V2s'])[:leng+1]
    yvals = arr[np.gradient(arr) < 0.005]
    xval = s['xy'][:leng+1,0][np.gradient(arr, edge_order=1) < 0.005]
    ax.fill_between(xval, yvals-0.02, yvals + 0.02, color='red', alpha=0.2, label='Adverse Pressure Gradient')

    arr2 = np.array(s['Vs_V2s'])[:leng-1:-1]
    yvals = arr2[np.gradient(arr2) > 0.01]
    xyarr = s['xy'][:leng-1:-1,0]
    xval = xyarr[np.gradient(arr2, edge_order=1) > 0.01]
    ax.fill_between(xval, yvals-0.02, yvals + 0.012, color='red', alpha=0.2)

    # plot regions of adverse pressure gradient

    # Plot the measured velocity distribution
    ax.plot(s['xy'][:,0],s['Vs_V2s'],'.-',color=cols[0,:],label='Measured')
    ax.legend()

    # Calculate diffusion factor
    V_max = np.nanmax(s['Vs_V2s']); V_2 = t['V2_V2s_av']
    s['D'] = (V_max - V_2) / V_max 

    # Integrate the pressures to determine force coefficients 
    s['Zx'] = np.trapz(s['Cp'],x=s['xy'][:,1])
    s['Zy'] = np.trapz(s['Cp'],x=s['xy'][:,0])

    # Record gas constants
    q = np.in1d(e['t'],e['t_lift'])
    s['R'] = e['R'][q]; s['T'] = e['T'][q]; s['ga'] = e['ga'][q];
    s['ro'] = e['Pa'][q] / (s['R'] * s['T'])

    # Isentropic surface velocities
    V2s = ((Po_1 - P_2) / (0.5 * s['ro']))**0.5
    s['Vs'] = s['Vs_V2s'] * V2s

    # Print quantities to screen
    print('3 - Blade Surface Pressure Distribution\n\nProcessed from blade tappings & tunnel')
    print('D = %4.3f , Zx = %4.3f , Zy = %4.3f\n\n' 
        % (s['D'],s['Zx'],s['Zy']))

    return(s,h)


def reynolds_number(t,b):
    # Sensitivity of cascade to Reynolds number

    # Assume constant dynamic viscosity of air
    mu = 18.8e-6

    # Figure window for loss sensitivity
    h = plt.figure('Reynolds Sensitivity'); ax = plt.gca();
    set_axes(ax,r'$\rho V_2 C / \mu$','($P_{01} - P_{02}$) / ($P_{01} - P_{2,av}$)')
    cols = gen_cols()

    # Log scale axes settings
    ax.set_xscale('log'); ax.set_ylim((0,0.035));
    ax.xaxis.grid(True, which='minor')

    # Plot existing data from high speed tests 
    ax.plot(b['reynolds']['Re'],b['reynolds']['Yp'],'.-',
        color=cols[1,:],label='$M_2 = 0.8$')

    # Calculate Reynolds number of current test
    t['Re'] = np.mean(t['ro']) * np.mean(t['V_2']) * b['geom']['c'] * 1e-3 / mu 

    # Calculate exit Mach number too
    t['M_2'] = np.mean(t['V_2']) / \
        (np.mean(t['ga']) * np.mean(t['R']) * np.mean(t['T']))**0.5 

    # Plot the current test
    lab = "$M_2 = %3.2f$" % t['M_2']
    ax.plot(t['Re'],t['Yp_av'],'o',color=cols[0,:],label=lab)
    ax.legend()

    return(t,h)


def mach_number(s,t,b):
    # Sensitivity of cascade to Mach number

    # Figure window for mach distributions
    h = plt.figure('Mach Distribution'); ax = plt.gca();
    set_axes(ax,'x / Cx','$M_s$')
    cols = gen_cols()

    # Plot existing data from high speed tests 
    for n in range(b['M'].shape[1]):
        if n == 0:
            lab = 'Variable Density Tunnel'
        else:
            lab = ''
        ax.plot(b['x'][:,n],b['M'][:,n],'.-',
            color=cols[1,:],label=lab)

    # Isentropic surface Mach distribution
    s['Ms'] = s['Vs'] / (s['ga'] * s['R'] * s['T'])**0.5 

    # Plot the current test
    ax.plot(s['xy'][:,0],s['Ms'],'.-',
        color=cols[0,:],label='4A3 Tunnel')
    ax.legend()

    return(s,h)


def channels(N):
    # Convert all channel numbers to python indices

    # Loop over all keys, minus 1 and convert to integers
    for instr in N.keys():
        for chan in N[instr]:
            N[instr][chan] = N[instr][chan] - 1
            N[instr][chan] = N[instr][chan].astype(int)

    return(N)


def gen_cols():
    # Generate array for colourmap of lines

    # RGB values
    cols = np.array([[0,0.447,0.741],
            [0.85,0.325,0.098],
            [0.929,0.694,0.125],
            [0.494,0.184,0.556],
            [0.466,0.674,0.188],
            [0.301,0.745,0.933],
            [0.635,0.078,0.184],
            [0,0.447,0.741]])

    return(cols)

def plot_blade(ax,e, pos):

    # Plot the suction surface
    xys = np.array(e['xy_ss'])
    xyp =  np.array(e['xy_ps'])
    # concate the two arrays but reverse the second one
    all_xy = np.concatenate((xys,xyp[::-1,:]),axis=0)
    # offset all points by pos
    Cx = 30.323 # mm
    all_xy = Cx * all_xy + np.array(pos)
    
    # plot the blade as closed plot
    ax.plot(all_xy[:,0],all_xy[:,1],'k-')
    ax.fill(all_xy[:,0],all_xy[:,1],color='grey',alpha=0.5)

    return(ax)

def set_axes(ax,xlab,ylab):
    # Format axes

    # Add axes labels
    ax.set_xlabel(xlab); ax.set_ylabel(ylab);

    # Format grid and ticks
    ax.grid(linestyle='-',color=[0.6,0.6,0.6],linewidth=0.5)
    ax.tick_params(direction='in')

    return(ax)


def main():

    # Specify directory and filename of run to process
    data_dir = 'IIB/4A3/turbine_cascade/data/'
    fig_dir = 'IIB/4A3/turbine_cascade/figures/'
#    directory = '/home/james/Documents/Teaching/4A3/4A3_Results/'
    filename = '4A3_cascade_lwp26_jrt66_30-Oct-2024_1.mat'

    # Read the experimental data
    e = mat73.loadmat(data_dir + filename); e = e['e'];

    # Load cascade geometry and CFD data
    b = mat73.loadmat(data_dir + 'cascade.mat'); b = b['b'];

    # Convert all channel numbers
    N = channels(e['N'])

    # Initialise plotting variables
    dpi = 400; ext = '.png';

    # 1 - General calculations
    general(e,N)

    # 2 - Exit traverse
    t,h = exit_traverse(e,N,b['geom'])

    # 3 - Blade surface pressure distribution
    s,h['lift'] = lift_distribution(e,N,t,b['cfd'])

    # 4 - Effect of Reynolds number
    t,h['reynolds'] = reynolds_number(t,b)

    # 5 - Effect of Mach number
    s,h['mach'] = mach_number(s,t,b['mach'])

    # Save the plots to file
    for name in h.keys():
        h[name].savefig(fig_dir + name + '_plot' + ext,dpi=dpi)
    
    # Show all the plots
    plt.show()

    
main()


