

representative_longitudinal_den = [1 1.6366 3.4115 0.07937 0.05112];
elev_normal_tf = - tf([0.0139 -0.0693 -0.4071 -0.0242 0], representative_longitudinal_den);
elev_pitch_tf = -tf([-2.637 -2.475 -0.0607], representative_longitudinal_den);



G = He * (elev_normal_tf + s*(12.4 + 1.65 * s) * elev_pitch_tf);

figure;
rlocus(G);

