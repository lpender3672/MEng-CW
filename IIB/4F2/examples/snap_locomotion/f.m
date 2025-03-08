function [y] = f(u)

%parameters
gamma = 5;
A = [0 1 0; 0 -10 1; -gamma 0 0];
B = [0 ; -1 ; 0];


%input parsing
w = u(1);
x = [u(2);u(3);u(4)];

%behavior
dx = A*x + B*w;

%outout derivatives
y = [dx];
end

