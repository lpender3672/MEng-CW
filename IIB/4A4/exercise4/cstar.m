
close all;

s = tf('s');

elev_normal_tf = -tf(elevator_to_normal_num, longitudinal_den);
%elev_pitchrate_tf = -tf(elev_to_pitchrate_num, longitudinal_den);
elev_pitchrate_tf = tf([-2.637 -2.475 -0.0607], longitudinal_den);

tau_e = 0.1;
He = 1 / (tau_e * s + 1);

G = He * (elev_normal_tf + 12.4 * elev_pitchrate_tf + 1.65 * s * elev_pitchrate_tf);

%w = makeweight(10, 0.1, 0.9);
%bode(w)
% Compensator adds a pole in the RHP to invert phugoid pole locus out of
% the RHP. This is 

%figure;
%nyquist(0.04*G, 0.1 * w * G);

figure;
%Gsubs = feedback(0.8 * G, 1);
rlocus(G);

figure;
hold on;


for k = [0.08]
    CL = feedback(k * G, 1);
    
    [Y,T] = step(CL, 20);
    step(CL, 20);
    
    [~, tis3] = min((T-3).^2);
    
    [cst,cslo,csup] = csenv(Y(tis3));
    plot(cst, cslo, 'g');
    plot(cst, csup, 'r');
    
end
xlim([0, 3]);
hold off; grid on;

figure;
step(CL);
