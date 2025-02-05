

% State space model
A = [0 1; 4 0];
B = [1;-1];
C = [1 0];
D = 0;

% Cost function
Q = C'*C;
R = 1;
iR = inv(R);

% Terminal cost
XN_1 = 30*eye(2);
XN_2 = zeros(2);

% Discretisation time step
dt = 0.001;
T = 4;

% The "discretised" grid of time steps
trange = 0:dt:T;

% Integrate the Riccati equation backwards
Xlog_1 = lqr_backwards_sweep(A,B,Q,R,XN_1, dt, trange);
Xlog_2 = lqr_backwards_sweep(A,B,Q,R,XN_2, dt, trange);

% Run the system forwards
x0 = [1;1];         % Initial conditions
[xlog_1,ulog_1] = lqr_forwards_sim(A, B, R, x0, Xlog_1, dt, trange);
[xlog_2,ulog_2] = lqr_forwards_sim(A, B, R, x0, Xlog_2, dt, trange);


% Do some plotting

figure;
subplot(3,2,1);
plot(trange, squeeze(Xlog_1(1,1,:)), 'k'); hold on;
plot(trange, squeeze(Xlog_1(1,2,:)), 'k--');
plot(trange, squeeze(Xlog_1(2,2,:)), 'k:');
xlabel('t');
ylabel('X(t)');
legend('X(1,1)', 'X(1,2)', 'X(2,2)', 'Location', 'NorthWest');
set(gca, 'Ylim', [0 60]);
title('X(4) = diag([30 30])');

subplot(3,2,2);
plot(trange, squeeze(Xlog_2(1,1,:)), 'k'); hold on;
plot(trange, squeeze(Xlog_2(1,2,:)), 'k--');
plot(trange, squeeze(Xlog_2(2,2,:)), 'k:');
xlabel('t');
ylabel('X(t)');
legend('X(1,1)', 'X(1,2)', 'X(2,2)', 'Location', 'NorthWest');
set(gca, 'Ylim', [0 60]);
title('X(4) = diag([0 0])');


subplot(3,2,3);
plot(trange, squeeze(xlog_1(1,:)), 'k'); hold on;
plot(trange, squeeze(xlog_1(2,:)), 'k--');
xlabel('t');
ylabel('x(t)');
legend('x_1', 'x_2');
set(gca, 'Ylim', [-2 4]);

subplot(3,2,4);
plot(trange, squeeze(xlog_2(1,:)), 'k'); hold on;
plot(trange, squeeze(xlog_2(2,:)), 'k--');
xlabel('t');
ylabel('x(t)');
legend('x_1', 'x_2');
set(gca, 'Ylim', [-2 4]);



subplot(3,2,5);
plot(trange(1:end-1), squeeze(ulog_1(1,:)), 'k'); hold on;
xlabel('t');
ylabel('u(t)');
set(gca, 'Ylim', [-15 5]);


subplot(3,2,6);
plot(trange(1:end-1), squeeze(ulog_2(1,:)), 'k'); hold on;
xlabel('t');
ylabel('u(t)');
set(gca, 'Ylim', [-15 5]);

set(gcf, 'PaperUnits', 'centimeters');
set(gcf, 'PaperPosition', [0 0 18 24]);

