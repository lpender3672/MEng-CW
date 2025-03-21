
close all;

s = tf('s');
elev_pitch_tf = - 1/s * tf([-2.637 -2.475 -0.0607, 0], longitudinal_den);

tau_e = 0.1;
He = 1 / (tau_e * s + 1);

T = 10;
integrator = (1 + 1/(T*s));
G = He * integrator * elev_pitch_tf;

figure;
rlocus(G);
sgrid([0.4], []);

k = 1.4;
CL = feedback(k * integrator * G, 1);

figure;
hold on;
step(CL);
yline(1.1, '--', 'Overshoot limit');
yline(0.95, '--', 'Subsequent Overshoot');

hold off;

