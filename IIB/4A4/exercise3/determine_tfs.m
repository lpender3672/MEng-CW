

clear all;
close all;

SPPO_corrected = load("SPPO_deltae_to_theta.mat");
SPPO = load("data_2024/SPPO.mat");
Spiral = load("data_2024/Spiral.mat");
RollSubs = load("data_2024/Roll-Subs.mat");
Phugoid = load("data_2024/Phugoid.mat");
DutchRoll = load("data_2024/Dutch-Roll.mat");

zeta_spo = 0.441;
omega_spo_n = 1.836;
zeta_phu = 0.066;
omega_phu_n = 0.123;

spoa = -zeta_spo * omega_spo_n;
spob = omega_spo_n * sqrt(1- zeta_spo^2);
phua = -zeta_phu * omega_phu_n;
phub = omega_phu_n * sqrt(1- zeta_phu^2);

long_roots = [spoa + 1j * spob, spoa - 1j * spob, phua + 1j * phub, phua - 1j * phub];
longitudinal_den = real(poly(long_roots));

zeta_dut = 0.150;
omega_dut_n = 1.519;
Tspiral = 42.6;
Trollsubs = 0.2495;

duta = -zeta_dut * omega_dut_n;
dutb = omega_dut_n * sqrt(1- zeta_dut^2);

lat_roots = [-1/Tspiral, -1/Trollsubs, duta + 1j * dutb, duta - 1j * dutb];
lateral_den = real(poly(lat_roots));

%% elevator angle to pitch angle

figure;
hold on;
plot(SPPO_corrected.Time, SPPO_corrected.Elevator); plot(SPPO_corrected.Time,  SPPO_corrected.Ptchrt);
hold off;
legend("Elevator [deg]", "Pitch rate [deg/s]");
xlabel('Time (s)')

Elevator = SPPO_corrected.Elevator - mean(SPPO_corrected.Elevator(SPPO_corrected.Time < 1.8));
Ptchrt = SPPO_corrected.Ptchrt - mean(SPPO_corrected.Ptchrt(SPPO_corrected.Time < 1.8));

figure;
[omega, elev_to_pitchrate] = xfer(SPPO_corrected.Time, Elevator, Ptchrt);
[num1, elev_to_pitchrate_fit] = plotBode(omega, elev_to_pitchrate, longitudinal_den, 15, 3);
order1 = size(num1, 2) - 1;
grid on;


%% elevator angle to normal acceleration at IRS location
figure;
hold on;
plot(SPPO.Time, SPPO.Elevator); plot(SPPO.Time,  SPPO.Nz);
hold off;
legend("Elevator [deg]", "Normal Acceleration [g]");
xlabel('Time (s)')

Elevator = SPPO.Elevator - mean(SPPO.Elevator(SPPO.Time > 10));
Nz = SPPO.Nz - mean(SPPO.Nz(SPPO.Time > 10));

figure;
[omega, elevator_to_normal] = xfer(SPPO.Time, Elevator, Nz);
[num2, elevator_to_normal_fit] = plotBode(omega, elevator_to_normal, longitudinal_den, 15, 3);
grid on;


%% rudder angle to yaw rate DutchRoll
figure;
hold on;
plot(DutchRoll.Time, DutchRoll.Rudder); plot(DutchRoll.Time,  DutchRoll.Yawrt);
hold off;
legend("Rudder [deg]", "Yaw rate [deg/s]");
xlabel('Time (s)')

Rudder = DutchRoll.Rudder - mean(DutchRoll.Rudder(DutchRoll.Time > 20));
Yawrt = DutchRoll.Yawrt - mean(DutchRoll.Yawrt(DutchRoll.Time < 19));

figure;
[omega, rudder_to_yawrate] = xfer(DutchRoll.Time, Rudder, Yawrt);
plotBode(omega, rudder_to_yawrate, lateral_den, 15, 3);
grid on;


%% aileron angle to roll angle RollSubs

figure;
hold on;
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
plotBode(omega, aileron_to_rollrate, lateral_den, 20, 3);
hold off;
grid on;
