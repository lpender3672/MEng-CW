% Constants
g = 9.81;   % m/s^2
L = 0.125;  % distance from pendulum's centre of mass to pivot in m
a = 0.016;  % radius of pulley in m
m = 0.32;   % mass of pendulum in kg
M = 0.7;    % mass of carriage in kg
I = 8e-5;   % moment of inertia on motor shaft in kg m^2
km = 0.08;  % torque motor constant in Nm/A
ka = -0.50; % amplifier constant in A/V
gamma = M/m + I/(m*a^2);

% State-space matrices
omega_1 = sqrt(g/L);
omega_0 = omega_1 * sqrt(1 + 1/gamma);

Ac = [0, 1, 0, 0;
      0, 0, omega_1^2 - omega_0^2, 0;
      0, 0, 0, 1;
      0, 0, -omega_0^2, 0];

B = [0; 1; 0; 1];

Sc = diag([-1/12.5, -1/2.23, L/3.18, L/0.64]);

opamp_c = diag([-20, -30, 20, -10]);  % for crane controller

Cc = -(ka*km/(m*a*gamma)) * (Sc \ opamp_c);

% Create state-space model
sys = ss(Ac, B, Cc, 0);

% Define gain range for k2
p2_range = [-logspace(5, -3, 1000), logspace(-3, 5, 1000)];  % Adjust the range and number of gains as needed

% Set fixed values for k1, k3, and k4

alpha = 10; beta = 10; omega = 10;
om12 = omega_1^2; om02 = omega_0^2;
k1 = 2*omega^2*alpha*beta/om12;
k2 = (2*omega^2*(alpha+beta)+2*omega*alpha*beta)/om12;
k3 = 2*omega^2+2*omega*(alpha+beta)+alpha*beta-om02-k1;
k4 = 2*omega+alpha+beta-k2;

P = [k1, k2, k3, k4] / Cc;
p1 = P(1); p2 = P(2); p3 = P(3); p4 = P(4);

P

figure;
hold on;
for p2_iter = p2_range
    P_p = [p1, p2_iter, p3, p4];
    eig_values_p = eig(Ac - B * P_p * Cc);
    if p2_iter > 0
        plot(real(eig_values_p), imag(eig_values_p), 'b.', 'MarkerSize', 8);
    else
        plot(real(eig_values_p), imag(eig_values_p), 'r.', 'MarkerSize', 8);
    end
end

eig_values_p = eig(Ac - B * P * Cc);
plot(real(eig_values_p), imag(eig_values_p), 'g.', 'MarkerSize', 16);

xlabel('Real');
ylabel('Imaginary');
xlim([-30,40]);
ylim([-30,30])
title('Eigenvalue Locations for Different Values of p_2');
grid on;
