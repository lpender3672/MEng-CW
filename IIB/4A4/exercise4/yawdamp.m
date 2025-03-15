
close all;

rudder_yaw_tf = -tf(rudder_to_yawrate_num, lateral_den);
s = tf('s');

tau_r = 0.25;
Hr = 1 / (tau_r * s + 1);

G = Hr * rudder_yaw_tf;

figure;
rlocus(G);
sgrid([0.8, 0.4], []);

k = 1.66;
CL = feedback(k*G, 1);

figure;
impulse(CL, 20)

