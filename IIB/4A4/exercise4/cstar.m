
close all;

s = tf('s');

%elev_normal_tf = - tf(elevator_to_normal_num, longitudinal_den);
%elev_pitchrate_tf = -tf(elev_to_pitchrate_num, longitudinal_den);
%elev_pitch_tf = tf([-2.637 -2.475 -0.0607], [1 1.6366 3.4115 0.07937 0.05112]);

rep_elev_norm_num = -tf([-0.0139 -0.0693 -0.4071 -0.0242 0],1);
rep_evel_pitch_num = -tf([-2.637 -2.475 -0.0607], 1);
den = tf(1, [1 1.6366 3.4115 0.07937 0.05112]);

tau_e = 0.1;
He = 1 / (tau_e * s + 1);

G = He * den * (rep_elev_norm_num + pi/180 * s*(12.4 + (1.65/9.81) * s) * rep_evel_pitch_num);


%w = makeweight(10, 0.1, 0.9);
%bode(w)
% Compensator adds a pole in the RHP to invert phugoid pole locus out of
% the RHP. This is 

%figure;
%nyquist(0.04*G, 0.1 * w * G);

%% RLOCUS
%Gsubs = feedback(0.8 * G, 1);
figure;
rlocus(G);
hold on;
k = 20;
r = rlocus(G, k);
h = plot(real(r), imag(r), 'v', 'MarkerSize', 5);
legend(h, ['k = ' num2str(k)])
hold off;
sgrid([0.4, 0.05, 0], [100, 100, 1]);
xlim([-60, 10])
ylim([-25,25])
print('exercise4\figures\cstar_base_rlocus', '-dpng', '-r600');
xlim([-0.06, 0.04])
ylim([-0.2, 0.2])
print('exercise4\figures\cstar_base_rlocus_zoomed', '-dpng', '-r600');


figure;
[cst,cslo,csup] = csenv(1.03);
xenv = [cst, flip(cst)];
yenv = [cslo, flip(csup)];
plot(xenv, yenv, 'g');

legend_labels = {'Envelope Bound'};

hold on;

for k = [ 4, 6, 20, 50]
    CL = feedback(k * G, 1);

    [Y,T] = step(CL, 10);
    [~, tis3] = min((T-3).^2);
    
    plot(T, Y/Y(tis3))

    legend_labels{end + 1} = ['k = ', num2str(k)];
end

xlim([0,3])
hold off; grid on;

legend(legend_labels, 'Location', 'best');
xlabel('Time (s)')
ylabel('Normalised C* (-)')

print('exercise4\figures\cstar_envelope_step', '-dpng', '-r600');


