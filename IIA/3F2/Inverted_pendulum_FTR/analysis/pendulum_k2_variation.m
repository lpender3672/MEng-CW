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

Ap = [0, 1, 0, 0;
      0, 0, omega_0^2 - omega_1^2, 0;
      0, 0, 0, 1;
      0, 0, omega_0^2, 0];

B = [0; 1; 0; 1];

opamp_p = diag([10, 20, 30, -20]);  % for inverted pendulum controller

Sp = diag([-1/12.5, -1/2.23, L/3.18, -L/0.64]);

Cp = -(ka*km/(m*a*gamma)) * (Sp \ opamp_p);

% Create state-space model
sys = ss(Ap, B, Cp, 0);

% Define gain range for k2
k2_range = [-logspace(3, -5, 500), logspace(-5, 3, 1500)];  % Adjust the range and number of gains as needed

% Set fixed values for k1, k3, and k4

k1 = - omega_1^2;
k2 = -4 * omega_1;
k3 = omega_0^2 + 7 * omega_1^2;
k4 = 8 * omega_1;

K = [k1, k2, k3, k4] / Cp;
k1 = K(1); k2 = K(2); k3 = K(3); k4 = K(4);

figure;
hold on;
for k2_iter = k2_range
    K_p = [k1, k2_iter, k3, k4];
    eig_values_p = eig(Ap - B * K_p * Cp);
    if k2_iter > 0
        plot(real(eig_values_p), imag(eig_values_p), 'b.', 'MarkerSize', 8);
    else
        plot(real(eig_values_p), imag(eig_values_p), 'r.', 'MarkerSize', 8);
    end
end

K_p = [k1, k2, k3, k4];
eig_values_p = eig(Ap - B * K_p * Cp);
plot(real(eig_values_p), imag(eig_values_p), 'g.', 'MarkerSize', 16);

xlabel('Real');
ylabel('Imaginary');
xlim([-30,50]);
ylim([-40,40])
title('Eigenvalue Locations for Different Values of k2');
grid on;
