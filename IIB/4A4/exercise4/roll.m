
close all;

% roll angle autopilot
s = tf('s');

aileron_roll_tf = -1/s * tf(aileron_to_rollrate_num, lateral_den);

tau_a = 0.05;
Ha = 1 / (tau_a * s + 1);

G = Ha * aileron_roll_tf;



figure;
rlocus(G);
sgrid([0.8, 0], [100, 1]);
xlim([-2.5, 0.5])
ylim([-5,5])
hold on;
k1=1.24;
k2 = 0.75;
r1 = rlocus(G, k1);
h1 = plot(real(r1), imag(r1), 'v', 'MarkerSize', 5);
r2 = rlocus(G, k2);
h2 = plot(real(r2), imag(r2), '^', 'MarkerSize', 5);
legend([h1, h2], {['k = ' num2str(k1)], ['k = ' num2str(k2)]}, 'Location', 'southeast')
hold off;
print('exercise4\figures\roll_autopilot_locus_uncompensated', '-dpng', '-r600');


figure;
hold on;
step(feedback(k1*G, 1));
step(feedback(k2*G, 1));
yline(1.1, '--', 'Overshoot limit');
yline(1.05, '--', 'Subsequent Overshoot');
legend({['k = ' num2str(k1)], ['k = ' num2str(k2)]}, 'Location', 'southeast')
hold off;
grid on;
print('exercise4\figures\roll_autopilot_step_uncompensated', '-dpng', '-r600');


%% Compensated:
% doesnt seem to need it


[Y, T] = step(CL);
step_response = stepinfo(Y,T);
rise_time = step_response.RiseTime;
settle_times = step_response.RiseTime;
peak_time = step_response.PeakTime;
overshoot = step_response.Overshoot;

