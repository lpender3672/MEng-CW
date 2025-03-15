
clear; close;

syms y z1 z2 s r

tau1 = 0.1; % slow first order network
tau2 = 0.01; % fast first order network

w1 = 1.0;
w2 = 1.0;
w3 = 1.0;

f = [-y + tanh(w1*z1 + w2*z2 + w3*y) + r;
     10 * (-z1 + y);
     100 * (-z2 + y)];

x = [y; z1; z2];

dy = jacobian(f, x);

