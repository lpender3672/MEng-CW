
close all;
% Rule-Based Autotuning Based on Frequency Domain Identification
% Anthony S. McCormack and Keith R. Godfrey

s = tf('s');

elev_pitch_tf = - 1/s * tf([-2.637 -2.475 -0.0607, 0], [1 1.6366 3.4115 0.07937 0.05112]);

tau_e = 0.1;
He = 1 / (tau_e * s + 1);

G = He * elev_pitch_tf;

rlocus(G)
sgrid([0.4, 0], [100, 1]);
grid on;
xlim([-1.2, 0.2])
ylim([-5, 5])

k_lim = 3.81;
T_lim = 2*pi / 3.4;

figure;

% classic Ziegler Nichols
kc = 0.6 * k_lim;
Ti = 0.5 * T_lim;
Td = 0.125 * T_lim;
K = kc * (1 + 1 / (Ti * s) + Td * s);
step(feedback(K*G, 1));

hold on;

% some overshoot
kc = 0.33 * k_lim;
Ti = 0.5 * T_lim;
Td = 0.33 * T_lim;
K = kc * (1 + 1 / (Ti * s) + Td * s);
step(feedback(K*G, 1))

% no overshoot
kc = 0.2 * k_lim;
Ti = 0.5 * T_lim;
Td = 0.33 * T_lim;
K = kc * (1 + 1 / (Ti * s) + Td * s);
step(feedback(K*G, 1))

kc = 0.2 * k_lim;
Ti = 0.5 * T_lim;
Td = 0.33 * T_lim;
K = kc * (1 + 1 / (Ti * s) + Td * s);
step(feedback(K*G, 1))
hold off;
yline(1.1, '--', 'Overshoot limit');
yline(1.05, '--', 'Subsequent Overshoot');

grid on;
legend('Ziegler Nichols', 'SO Rule', 'NO Rule')

print('exercise4\figures\pitch_autopilot_autotuning_comparison', '-dpng', '-r600');

