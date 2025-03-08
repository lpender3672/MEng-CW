function [y] = f(u)

%parameters
C = 0.1;
L = 1;

%input parsing
k = u(1);
x = u(2);
z = u(3);


%behavior equations
dx = 1/C * (-z - x^3 + k*x);
dz =  1/L * x;

%outout derivatives
y = [dx;dz];
end

