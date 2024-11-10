
import numpy as np
from scipy import interpolate

## This file will determine if buffeting occurs.


# Result.buffet_causes = ["difference in shock entry mach number to 1.2",
#                          "difference between Hbar_te and 2.2",
#                          "minimum distance between cp and line between [(0,1.5),(1,1.2)]",
#                          "cpte - cpte_plateau - 0.04, where cpte_plateau is the region of smoothed gradient below a threshhold",
#                          ""]

def mach_from_p_over_p0(p_over_p0):
    gamma = 1.4

    return np.sqrt((p_over_p0 ** (- (gamma - 1) / gamma) - 1) * 2 / (gamma - 1))


def mach_numbers_at_shocks(res):

    upsh = res.shock_locations['upper_shock_locations']
    losh = res.shock_locations['lower_shock_locations']

    mup = np.zeros(len(upsh))
    mlo = np.zeros(len(losh))

    i = 0
    for xup in upsh:
        p_over_p0 = res.p_over_p0[np.argmin(np.abs(res.x - xup))]
        mup[i] = mach_from_p_over_p0(p_over_p0)
        i += 1
    
    i = 0
    for xlo in losh:
        p_over_p0 = res.p_over_p0[np.argmin(np.abs(res.x - xlo))]
        mlo[i] = mach_from_p_over_p0(p_over_p0)
        i += 1

    return mup, mlo



def get_difference_in_shock_entry_mach_number_to_1_2(res):
    mup, _ = mach_numbers_at_shocks(res)
    return np.max(mup) - 1.2


def get_difference_between_Hbar_te_and_2_2(res):
    Hbar_te = res.boundary_layer_data['HBAR']
    return Hbar_te - 2.2

def get_min_distance_between_mach_lines(res):

    def f(x):
        return 1.5 + (1.2 - 1.5) / 1 * x
    
    lin_mach = f(res.x)
    machs = mach_from_p_over_p0(res.p_over_p0)
    dmachs = machs - lin_mach

    return np.max(dmachs)   

def get_difference_delta_cpte_above_threshold(res, cpte_plateau):
    # TODO: Implement
    raise NotImplementedError

def buffet_classification(res, cpte_plateau):

    res.buffet_causes = [
        get_difference_in_shock_entry_mach_number_to_1_2(res),
        get_difference_between_Hbar_te_and_2_2(res),
        get_min_distance_between_mach_lines(res),
        get_difference_delta_cpte_above_threshold(res, cpte_plateau)
    ]

    return res