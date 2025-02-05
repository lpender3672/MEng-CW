import sympy as sp
import control as ct
from matplotlib import pyplot as plt

# define 6 degrees of freedom
v = sp.symbols('v') # sideslip
w = sp.symbols('w') # heave
u = sp.symbols('u') # surge
phi = sp.symbols('phi') # roll
theta = sp.symbols('theta') # pitch
psi = sp.symbols('psi') # yaw

p = sp.symbols('p') # roll rate
q = sp.symbols('q') # pitch rate
r = sp.symbols('r') # yaw rate
v_dot = sp.symbols('v_dot')
w_dot = sp.symbols('w_dot')
u_dot = sp.symbols('u_dot')
p_dot = sp.symbols('p_dot')
q_dot = sp.symbols('q_dot')
r_dot = sp.symbols('r_dot')

# define control inputs
delta_e = sp.symbols('delta_e') # elevator
delta_a = sp.symbols('delta_a') # aileron
delta_r = sp.symbols('delta_r') # rudder

X_u = sp.symbols('X_u')
X_w = sp.symbols('X_w')
X_q = sp.symbols('X_q')
Z_u = sp.symbols('Z_u')
Z_w = sp.symbols('Z_w')
Z_q = sp.symbols('Z_q')
M_u = sp.symbols('M_u')
M_w = sp.symbols('M_w')
Y_v = sp.symbols('Y_v')
Y_p = sp.symbols('Y_p')
Y_r = sp.symbols('Y_r')
L_v = sp.symbols('L_v')
L_p = sp.symbols('L_p')
L_r = sp.symbols('L_r')
L_delta_a = sp.symbols('L_delta_a')
L_delta_R = sp.symbols('L_delta_r')
M_delta_e = sp.symbols('M_delta_e')

U = sp.symbols('U')
m = sp.symbols('m')
I_x = sp.symbols('I_x')
I_y = sp.symbols('I_y')
I_z = sp.symbols('I_z')
g = sp.symbols('g')


def create_lecture_equations():
    

    eq1 = sp.Eq(m * u_dot, X_u * u + X_w * w + X_q * q - m * g * theta)
    eq2 = sp.Eq(m * (w_dot- U * q), Z_u * u + Z_w * w + Z_q * q)
    eq3 = sp.Eq(I_y * q_dot, M_u * u + M_w * w + M_w * w_dot + M_delta_e * delta_e)
    eq4 = sp.Eq(m * (v_dot + U * r), Y_v * v + Y_p * p + Y_r * r + m * g * phi)
    eq5 = sp.Eq(I_x * p_dot, L_v * v + L_p * p + L_r * r + L_delta_a * delta_a + L_delta_R * delta_r)
    eq6 = sp.Eq(I_z * r_dot, L_v * v + L_p * p + L_r * r + L_delta_a * delta_a + L_delta_R * delta_r)

    f6 = sp.Eq(u_dot, sp.solve(eq1, u_dot)[0])
    f5 = sp.Eq(w_dot, sp.solve(eq2, w_dot)[0])
    f2 = sp.Eq(q_dot, sp.solve(eq3, q_dot)[0])
    f4 = sp.Eq(v_dot, sp.solve(eq4, v_dot)[0])
    f1 = sp.Eq(p_dot, sp.solve(eq5, p_dot)[0])
    f3 = sp.Eq(r_dot, sp.solve(eq6, r_dot)[0])


    return f1, f2, f3, f4, f5, f6

def fourth_order_longitudinal():


    _, dq, _, _, dw, du = create_lecture_equations()
    state_vector = sp.Matrix([u, w, theta, q])
    input_vector = sp.Matrix([delta_e])
    output_vector = sp.Matrix([theta, q])

    state_vector_dot = sp.Matrix([du.rhs, dw.rhs, q, dq.rhs]) # thetadot = q

    # jacobi matrix
    A = state_vector_dot.jacobian(state_vector)
    B = state_vector_dot.jacobian(input_vector)
    C = output_vector.jacobian(state_vector)

    check = A * state_vector + B * input_vector
    assert (check - state_vector_dot).simplify() is None

    return A, B, C

def example_substitution_to_ss(A, B, C):

    A = A.subs([(X_u, -0.1), (X_w, -0.5), (X_q, 0), (Z_u, -0.1), (Z_w, -1), (Z_q, -1), (M_u, 0), (M_w, -0.5), (M_delta_e, -1), (Y_v, -0.1), (Y_p, 0), (Y_r, 0), (L_v, 0), (L_p, -0.5), (L_r, 0), (L_delta_a, 0), (L_delta_R, 0), (U, 1), (m, 1), (I_x, 1), (I_y, 1), (I_z, 1), (g, 9.81)])
    B = B.subs([(X_u, -0.1), (X_w, -0.5), (X_q, 0), (Z_u, -0.1), (Z_w, -1), (Z_q, -1), (M_u, 0), (M_w, -0.5), (M_delta_e, -1), (Y_v, -0.1), (Y_p, 0), (Y_r, 0), (L_v, 0), (L_p, -0.5), (L_r, 0), (L_delta_a, 0), (L_delta_R, 0), (U, 1), (m, 1), (I_x, 1), (I_y, 1), (I_z, 1), (g, 9.81)])
    C = C.subs([(X_u, -0.1), (X_w, -0.5), (X_q, 0), (Z_u, -0.1), (Z_w, -1), (Z_q, -1), (M_u, 0), (M_w, -0.5), (M_delta_e, -1), (Y_v, -0.1), (Y_p, 0), (Y_r, 0), (L_v, 0), (L_p, -0.5), (L_r, 0), (L_delta_a, 0), (L_delta_R, 0), (U, 1), (m, 1), (I_x, 1), (I_y, 1), (I_z, 1), (g, 9.81)])

    sys = ct.StateSpace(A, B, C, 0)
    return sys

def plot_step_response(sys):
    t, y = ct.step_response(sys)
    y = y[:,0,:]
    plt.plot(t, y.T)
    plt.show()

def test_fourth_order_longitudinal():
    A, B, C = fourth_order_longitudinal()
    sys = example_substitution_to_ss(A, B, C)
    print(sys)
    plot_step_response(sys)

test_fourth_order_longitudinal()
