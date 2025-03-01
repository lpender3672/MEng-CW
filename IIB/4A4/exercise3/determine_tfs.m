

clear all;
close all;

SPPO = load("SPPO_deltae_to_theta.mat");
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

roots = [spoa + 1j * spob, spoa - 1j * spob, phua + 1j * phub, phua - 1j * phub];
den = real(poly(roots));

%% elevator angle to pitch angle

figure;
hold on;
plot(SPPO.Time, SPPO.Elevator); plot(SPPO.Time,  SPPO.Ptchrt);
hold off;
legend("Elevator [deg]", "Pitch rate [deg/s]");
xlabel('Time (s)')

Elevator = SPPO.Elevator - mean(SPPO.Elevator(SPPO.Time < 1.8));
Ptchrt = SPPO.Ptchrt - mean(SPPO.Ptchrt(SPPO.Time < 1.8));

figure;
[omega, elev_to_pitchrate] = xfer(SPPO.Time, Elevator, Ptchrt);
plotBode(omega, elev_to_pitchrate, den, 15, 3);
grid on;


%% elevator angle to normal acceleration at IRS location
figure;
hold on;
plot(Phugoid.Time, Phugoid.Elevator); plot(Phugoid.Time,  Phugoid.Nz);
hold off;
legend("Elevator [deg]", "Normal Acceleration [g]");
xlabel('Time (s)')

Elevator = Phugoid.Elevator - mean(Phugoid.Elevator(Phugoid.Time > 30));
Nz = Phugoid.Nz - mean(Phugoid.Nz(Phugoid.Time > 30));figure;

figure;
[omega, elevator_to_normal] = xfer(Phugoid.Time, Elevator, Nz);
plotBode(omega, elevator_to_normal, den, 15, 3);
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
plotBode(omega, rudder_to_yawrate, den, 15, 3);
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
plotBode(omega, aileron_to_rollrate, den, 20, 3);
hold off;
grid on;
