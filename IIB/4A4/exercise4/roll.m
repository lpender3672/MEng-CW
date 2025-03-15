
% roll angle autopilot
s = tf('s');

aileron_roll_tf = -1/s * tf(aileron_to_rollrate_num, lateral_den);

tau_a = 0.05;
Ha = 1 / (tau_a * s + 1);

G = Ha * aileron_roll_tf;

figure;
rlocus(G);

k=1.3;
CL = feedback(k*G, 1);

figure;
step(CL)

[Y, T] = step(CL);
step_response = stepinfo(Y,T);
rise_time = step_response.RiseTime;
settle_times = step_response.RiseTime;
peak_time = step_response.PeakTime;
overshoot = step_response.Overshoot;

