
close;

elev_pitchrate_tf = tf(elev_to_pitchrate_num, longitudinal_den);
s = tf('s');

tau_e = 0.1;
He = 1 / (tau_e * s + 1);

Gsubs = He * elev_pitchrate_tf;

figure;
rlocus(Gsubs)