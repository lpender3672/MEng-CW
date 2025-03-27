
close all;

s = tf('s');

elev_pitch_tf_bad = - 1/s * tf(elev_to_pitchrate_num, longitudinal_den);


elev_pitch_tf = - 1/s * tf([-2.637 -2.475 -0.0607, 0], [1 1.6366 3.4115 0.07937 0.05112]);

tau_e = 0.1;
He = 1 / (tau_e * s + 1);

Ti = 10;
integrator = (1 + 1/(Ti*s));

Gbad = He * elev_pitch_tf_bad;
figure;
rlocus(Gbad);
sgrid([0.4, 0], [100, 1]);
grid on;
xlim([-1.2, 0.2])
ylim([-5, 5])
print('exercise4\figures\pitch_autopilot_locus_bad', '-dpng', '-r600');

Gibad = He * integrator * elev_pitch_tf_bad;
figure;
rlocus(Gibad);
sgrid([0.4, 0], [100, 1]);
grid on;
xlim([-1.2, 0.2])
ylim([-5, 5])
print('exercise4\figures\pitch_autopilot_locus_intbad', '-dpng', '-r600');
Gi = He * integrator * elev_pitch_tf;

%% uncompensated
k = 0.11;

figure;
rlocus(Gi);
sgrid([0.4, 0], [100, 1]);
grid on;
hold on;
xlim([-1, 0.2])
ylim([-5, 5])
r = rlocus(Gi, k);
h = plot(real(r), imag(r), 'v', 'MarkerSize', 5);
legend(h, ['k = ' num2str(k)])
hold off;
print('exercise4\figures\pitch_autopilot_locus_Ti', '-dpng', '-r600');

CL = feedback(k * Gi, 1);

figure;
hold on;
step(CL);
yline(1.1, '--', 'Overshoot limit');
yline(1.05, '--', 'Subsequent Overshoot');
ylim([0, 1.2])
grid on;
hold off;
print('exercise4\figures\pitch_autopilot_uncompensated_step', '-dpng', '-r600');

[Y, T] = step(CL);
disp(stepinfo(Y,T).RiseTime);

%% derivative controller
k = 0.7;
Td = 0.5;

integrator_derivative = (1 + 1/(Ti*s) + Td * s)
Gid = He * integrator_derivative * elev_pitch_tf;

figure;
rlocus(Gid);
sgrid([0.4, 0], [100, 1]);
grid on;
hold on;
r = rlocus(Gid, k);
h = plot(real(r), imag(r), 'v', 'MarkerSize', 5);
legend(h, ['k = ' num2str(k)])
hold off;
xlim([-5, 1])
ylim([-15, 15])
print('exercise4\figures\pitch_autopilot_locus_TiTd', '-dpng', '-r600');
xlim([-0.3, 0.1])
ylim([-0.6, 0.6])
print('exercise4\figures\pitch_autopilot_locus_TiTd_zoomed', '-dpng', '-r600');

CL = feedback(k * Gid, 1);
compute_margins(k * Gid)


figure;
hold on;
step(CL);
yline(1.1, '--', 'Overshoot limit');
yline(1.05, '--', 'Subsequent Overshoot');
ylim([0, 1.2])
grid on;
hold off;
print('exercise4\figures\pitch_autopilot_Ti10_Td01_step', '-dpng', '-r600');

[Y, T] = step(CL);
disp(stepinfo(Y,T).RiseTime);

%% compensated
alpha = 0.1;
Tc = 1;
lead_compensator = (Tc*s + 1) / (alpha * Tc * s + 1);
k = 0.7;
GIC = lead_compensator * He * integrator * elev_pitch_tf;
figure;
rlocus(GIC);
sgrid([0.4, 0], [100, 1]);
hold on;
grid on;
xlim([-2, 0.1])
ylim([-6, 6])
r = rlocus(GIC, k);
h = plot(real(r), imag(r), 'v', 'MarkerSize', 5);
legend(h, ['k = ' num2str(k)])
hold off;
print('exercise4\figures\pitch_autopilot_locus_compensated', '-dpng', '-r600');


compute_margins(k * GIC)

legend_labels = {};
figure;
hold on;

for k = [0.7]
    step(feedback(k*GIC, 1));

    legend_labels{end + 1} = ['k = ', num2str(k)];
end

yline(1.1, '--', 'Overshoot limit');
yline(1.05, '--', 'Subsequent Overshoot');
ylim([0, 1.2])
grid on;
hold off;
legend(legend_labels, 'Location','best')
print('exercise4\figures\pitch_autopilot_compensated_step', '-dpng', '-r600');



function [GM, PM, Wcg, Wcp] = compute_margins(G)

    [GM, PM, Wcg, Wcp] = margin(G);
    
    disp(['Gain Margin (GM): ', num2str(GM), ' dB']);
    disp(['Phase Margin (PM): ', num2str(PM), ' degrees']);
    disp(['Gain Crossover Frequency (Wcg): ', num2str(Wcg), ' rad/s']);
    disp(['Phase Crossover Frequency (Wcp): ', num2str(Wcp), ' rad/s']);
    
end