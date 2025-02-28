

clear all;
close all;

SPPO = load("SPPO_deltae_to_theta.mat");
Spiral = load("data_2024/Spiral.mat");
RollSubs = load("data_2024/Roll-Subs.mat");
Phugoid = load("data_2024/Phugoid.mat");
DutchRoll = load("data_2024/Dutch-Roll.mat");

%% elevator angle to pitch angle

[omega, elev_to_pitchrate] = xfer(SPPO.Time, SPPO.Elevator, SPPO.Ptchrt);
plot(omega, 20 * log10(abs(elev_to_pitchrate)));
xlabel('Frequency [rad/s]');
ylabel('Magnitude [dB]');
title('elevator angle to pitch angle');
hold off;
grid on;


%% elevator angle to normal acceleration at IRS location

figure;
[omega, elevator_to_normal] = xfer(Phugoid.Time, Phugoid.Elevator, Phugoid.Nz);
plot(omega, 20 * log10(abs(elevator_to_normal)));
xlabel('Frequency [rad/s]');
ylabel('Magnitude [dB]');
title('elevator angle to normal acceleration at IRS location');
hold off;
grid on;


%% rudder angle to yaw rate DutchRoll

figure;
[omega, rudder_to_yawrate] = xfer(DutchRoll.Time, DutchRoll.Rudder, DutchRoll.Yawrt);
plot(omega, 20 * log10(abs(rudder_to_yawrate)));
xlabel('Frequency [rad/s]');
ylabel('Magnitude [dB]');
title('rudder angle to yaw rate DutchRoll');
hold off;
grid on;


%% aileron angle to roll angle RollSubs

figure;
[omega, aileron_to_rollrate] = xfer(RollSubs.Time, RollSubs.Aileron, RollSubs.Rollrt);
plot(omega, 20 * log10(abs(aileron_to_rollrate)));
xlabel('Frequency [rad/s]');
ylabel('Magnitude [dB]');
title('aileron angle to roll angle RollSubs');
hold off;
grid on;
