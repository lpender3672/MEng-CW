

clear all;
close all;

SPPO_corrected = load("SPPO_deltae_to_theta.mat");
SPPO = load("data_2024/SPPO.mat");
Spiral = load("data_2024/Spiral.mat");
RollSubs = load("data_2024/Roll-Subs.mat");
Phugoid = load("data_2024/Phugoid.mat");
DutchRoll = load("data_2024/Dutch-Roll.mat");

% provided values
%zeta_spo = 0.441;
%omega_spo_n = 1.836;
%zeta_phu = 0.066;
%omega_phu_n = 0.123;
%zeta_dut = 0.150;
%omega_dut_n = 1.519;
%Tspiral = 42.6;
%Trollsubs = 0.2495;
elev_to_pitchrate_freq_cutoff = 10;
elevator_to_normal_freq_cutoff = 7;
rudder_to_yawrate_freq_cutoff = 3;
aileron_to_rollrate_freq_cutoff = 9;

% e2 values
zeta_spo = 0.429;
omega_spo_n = 2.23;
zeta_phu = 0.06;
omega_phu_n = 0.126;
zeta_dut = 0.12;
omega_dut_n = 1.52;
Tspiral = 42.6; % our values for the time consts were far off 
Trollsubs = 0.2495; % so we're just going to use theirs

spoa = -zeta_spo * omega_spo_n;
spob = omega_spo_n * sqrt(1- zeta_spo^2);
phua = -zeta_phu * omega_phu_n;
phub = omega_phu_n * sqrt(1- zeta_phu^2);

long_roots = [spoa + 1j * spob, spoa - 1j * spob, phua + 1j * phub, phua - 1j * phub];
longitudinal_den = real(poly(long_roots));

duta = -zeta_dut * omega_dut_n;
dutb = omega_dut_n * sqrt(1- zeta_dut^2);

% spiral is naturally unstable
lat_roots = [+1/Tspiral, -1/Trollsubs, duta + 1j * dutb, duta - 1j * dutb];
lateral_den = real(poly(lat_roots));

%% elevator angle to pitch angle

figure;
hold on;
grid on;
plot(SPPO_corrected.Time, SPPO_corrected.Elevator); plot(SPPO_corrected.Time,  SPPO_corrected.Ptchrt);
hold off;
legend("Elevator [deg]", "Pitch rate [deg/s]");
xlabel('Time (s)')

Elevator = SPPO_corrected.Elevator - mean(SPPO_corrected.Elevator(SPPO_corrected.Time < 1.8));
Ptchrt = SPPO_corrected.Ptchrt - mean(SPPO_corrected.Ptchrt(SPPO_corrected.Time < 1.8));

figure;
[omega, elev_to_pitchrate] = xfer(SPPO_corrected.Time, Elevator, Ptchrt);
hold on;
[elev_to_pitchrate_num, ~] = plotBode(omega, elev_to_pitchrate, longitudinal_den, elev_to_pitchrate_freq_cutoff, 3, ...
    '$|q/ \delta_E|$', '$\arg\left(\frac{q}{\delta_E}\right)$');
xline(elev_to_pitchrate_freq_cutoff);
hold off;
grid on;
print('exercise3\elev_to_pitchrate', '-dpng', '-r600');

%% elevator angle to normal acceleration at IRS location
figure;
hold on;
grid on;
plot(SPPO.Time, SPPO.Elevator); plot(SPPO.Time,  SPPO.Nz);
hold off;
legend("Elevator [deg]", "Normal Acceleration [g]");
xlabel('Time (s)')

Elevator = SPPO.Elevator - mean(SPPO.Elevator(SPPO.Time > 10));
Nz = SPPO.Nz - mean(SPPO.Nz(SPPO.Time > 10));

figure;
[omega, elevator_to_normal] = xfer(SPPO.Time, Elevator, Nz);
hold on;
[elevator_to_normal_num, ~] = plotBode(omega, elevator_to_normal, longitudinal_den, elevator_to_normal_freq_cutoff, 4, ...
    '$|n_z/ \delta_E|$', '$\arg\left(\frac{n_z}{\delta_E}\right)$');
xline(elevator_to_normal_freq_cutoff);
hold off;
grid on;
print('exercise3\elevator_to_normal', '-dpng', '-r600');


%% rudder angle to yaw rate DutchRoll
figure;
hold on;
grid on;
plot(DutchRoll.Time, DutchRoll.Rudder); plot(DutchRoll.Time,  DutchRoll.Yawrt);
hold off;
legend("Rudder [deg]", "Yaw rate [deg/s]");
xlabel('Time (s)')

Rudder = DutchRoll.Rudder - mean(DutchRoll.Rudder(DutchRoll.Time > 20));
Yawrt = DutchRoll.Yawrt - mean(DutchRoll.Yawrt(DutchRoll.Time < 19));

figure;
[omega, rudder_to_yawrate] = xfer(DutchRoll.Time, Rudder, Yawrt);
hold on;
[rudder_to_yawrate_num,~] = plotBode(omega, rudder_to_yawrate, lateral_den, rudder_to_yawrate_freq_cutoff, 3, ...
    '$|r/ \delta_R|$', '$\arg\left(\frac{r}{\delta_R}\right)$');
xline(rudder_to_yawrate_freq_cutoff);
hold off;
grid on;
print('exercise3\rudder_to_yawrate', '-dpng', '-r600');

%% aileron angle to roll angle RollSubs

figure;
hold on;
grid on;
plot(RollSubs.Time, RollSubs.Aileron); plot(RollSubs.Time,  RollSubs.Rollrt);
hold off;
legend("Aileron [deg]", "Roll rate [deg/s]");
xlabel('Time (s)')

Aileron = RollSubs.Aileron - mean(RollSubs.Aileron(RollSubs.Time < 1.6));
Rollrt = RollSubs.Rollrt - mean(RollSubs.Rollrt(RollSubs.Time < 1.6));

freq4 = 2*pi/mean(diff(RollSubs.Time)); % ok so xfer handles the nyquist frequency
% also low frequencies will have poor resolution because of the relatively small
% window. Also close to the nyquist frequency will also be wrong

figure;
[omega, aileron_to_rollrate] = xfer(RollSubs.Time, Aileron, Rollrt);
hold on;
[aileron_to_rollrate_num,~] = plotBode(omega, aileron_to_rollrate, lateral_den, aileron_to_rollrate_freq_cutoff, 3, ...
    '$|p/ \delta_A|$', '$\arg\left(\frac{p}{\delta_A}\right)$');
xline(aileron_to_rollrate_freq_cutoff);
hold off;
grid on;
print('exercise3\aileron_to_rollrate', '-dpng', '-r600');


%% Final TFs
syms s

elev_to_pitchrate_tf = poly2sym(elev_to_pitchrate_num, s) / poly2sym(longitudinal_den, s);
elev_to_pitchrate_tf_tex = latex(vpa(elev_to_pitchrate_tf, 6))

elevator_to_normal_tf = poly2sym(elevator_to_normal_num, s) / poly2sym(longitudinal_den, s);
elevator_to_normal_tf_tex = latex(vpa(elevator_to_normal_tf, 6))

rudder_to_yawrate_tf = poly2sym(rudder_to_yawrate_num, s) / poly2sym(lateral_den, s);
rudder_to_yawrate_tf_tex = latex(vpa(rudder_to_yawrate_tf, 6))

aileron_to_rollrate_tf = poly2sym(aileron_to_rollrate_num, s) / poly2sym(lateral_den, s);
aileron_to_rollrate_tf_tex = latex(vpa(aileron_to_rollrate_tf, 6))
