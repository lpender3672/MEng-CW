
close all;

s = tf('s');
elev_pitch_tf = - 1/s * tf(elev_to_pitchrate_num, longitudinal_den);

tau_e = 0.1;
He = 1 / (tau_e * s + 1);

T = 100;
integrator = (1 + 1/(T*s))
G = He * integrator * elev_pitch_tf;

figure;
rlocus(G);
sgrid([0.4], []);

k = 0.1;
CL = feedback(k * integrator * G, 1);

figure;
step(CL);

