
close all;

rudder_yaw_tf = -tf(rudder_to_yawrate_num, lateral_den);
s = tf('s');

tau_r = 0.25;
Hr = 1 / (tau_r * s + 1);

G = Hr * rudder_yaw_tf;

figure;
rlocus(G);
sgrid([0.4, 0], [100, 0.4]);
grid on;
hold on;
k=1.66;
r = rlocus(G, k);
h = plot(real(r), imag(r), 'v', 'MarkerSize', 5);
legend(h, ['k = ' num2str(k)])
hold off;
print('exercise4\figures\yaw_damper_rlocus', '-dpng', '-r600');


legend_labels = {};
figure;
hold on;

for k = [0.882, 1.66, 4.76]
    impulse(feedback(k*G, 1), 20);
    legend_labels{end + 1} = ['k = ', num2str(k)];
end

legend(legend_labels, 'Location', 'southeast')
hold off;
grid on;
print('exercise4\figures\yaw_damper_impulse', '-dpng', '-r600');

