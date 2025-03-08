function [y] = f(u)

%parameters

tau1 = .1;
tau2 = 1;

%input parsing
k1 = u(1);
k2 = u(2);
x1 = u(3);
x2 = u(4);


%behavior equations
dx1 = 1/tau1 * (-x1 + sat(k1*x1 - k2*x2));
dx2 = 1/tau2 * (-x2 + sat(k1*x1 - k2*x2));

%outout derivatives
y = [dx1;dx2];
end

