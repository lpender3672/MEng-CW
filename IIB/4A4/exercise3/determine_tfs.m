

clear all;

SPPO = load("SPPO_deltae_to_theta.mat");
Spiral = load("data_2024/Spiral.mat");
RollSubs = load("data_2024/Roll-Subs.mat");
Phugoid = load("data_2024/Phugoid.mat");
DutchRoll = load("data_2024/Dutch-Roll.mat");

%% essentially just plotting F(y)/F(x) where F is fourier

[omega, elev_to_pitchrate] = xfer(SPPO.Time, SPPO.Elevator, SPPO.Ptchrt);
plot(omega, 20 * log10(abs(elev_to_pitchrate)));
xlabel('Frequency [rad/s]');
ylabel('Magnitude [dB]');
hold off;
grid on;
