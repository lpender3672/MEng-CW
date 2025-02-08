%% Load data
clear;

SPPO = load("data_2024/SPPO.mat");
Spiral = load("data_2024/Spiral.mat");
RollSubs = load("data_2024/Roll-Subs.mat");
Phugoid = load("data_2024/Phugoid.mat");
DutchRoll = load("data_2024/Dutch-Roll.mat");

%% SPO
figure;
hold on;
plot(SPPO.Time, SPPO.Ptchrt);
plot(SPPO.Time, SPPO.Elevator);
plot(SPPO.Time, SPPO.Alpha);
xlabel('Time [s]');
ylabel('');
legend('Pitch rate [\circ/s]', 'Elevator angle [\circ]', 'AoA [\circ]')
hold off;
grid on;
print('figures\SPO', '-dpng', '-r600');

%% Dutch Roll
figure;
hold on;
plot(DutchRoll.Time, DutchRoll.Rollang);
plot(DutchRoll.Time, DutchRoll.Rudder);
plot(DutchRoll.Time, DutchRoll.Rollrt);
xlabel('Time [s]');
ylabel('');
legend('Roll Angle [\circ]', 'Rudder angle [\circ]', 'Roll rate [\circ/s]')
hold off;
grid on;
print('figures\DutchRoll', '-dpng', '-r600');

%% Phugoid
figure;
hold on;
plot(Phugoid.Time, Phugoid.Ptchang);
plot(Phugoid.Time, Phugoid.Elevator);
xlabel('Time [s]');
ylabel('');
legend('Pitch angle [\circ]', 'Elevator angle [\circ]');
hold off;
grid on;

print('figures\Phugoid', '-dpng', '-r600');

%% Spiral
figure;
hold on;
plot(Spiral.Time, Spiral.Rollang);
plot(Spiral.Time, Spiral.Aileron);
plot(Spiral.Time, Spiral.Rollrt);

xlabel('Time [s]');
ylabel('');
legend('Roll angle [\circ]', 'Aileron angle [\circ]','Roll rate [\circ/s]');
hold off;
grid on;

print('figures\Spiral', '-dpng', '-r600');

%% Spiral log
figure;
hold on;
plot(Spiral.Time, log(Spiral.Rollang - Spiral.Rollang(1)));

xlabel('Time [s]');
ylabel('Log Roll angle');
hold off;
grid on;
    
print('figures\Spiral_log', '-dpng', '-r600');

%% Roll subsiding

figure;
hold on;
plot(RollSubs.Time, RollSubs.Rollang);
plot(RollSubs.Time, RollSubs.Aileron);
plot(RollSubs.Time, RollSubs.Rollrt);

xlabel('Time [s]');
ylabel('');
legend('Roll angle [\circ]', 'Aileron angle [\circ]','Roll rate [\circ/s]');
hold off;
grid on;
   
print('figures\RollSubs', '-dpng', '-r600');

%% Roll subsiding window

window = 10 < RollSubs.Time & RollSubs.Time < 13;
RSw_time = RollSubs.Time(window);
RSw_rollang = RollSubs.Rollang(window);
RSw_rollrt = RollSubs.Rollrt(window);

figure;
hold on;
plot(RSw_time, RSw_rollang);
xlabel('Time [s]');
ylabel('Roll angle [\circ]');
hold off;
grid on;
 
print('figures\RollSubs_window', '-dpng', '-r600');

%% Roll subsiding window log

window = 10 < RollSubs.Time & RollSubs.Time < 13;
RSw_time = RollSubs.Time(window);
RSw_rollang = RollSubs.Rollang(window);
RSw_rollrt = RollSubs.Rollrt(window);
    
figure;
hold on;
plot(RSw_time, log(RSw_rollang));
xlabel('Time [s]');
ylabel('Log windowed Roll angle [\circ]');
hold off;
grid on;
 
print('figures\RollSubs_logwindow', '-dpng', '-r600');
