
clear; close;

syms y z1 z2 w1 w2 w3 real
syms r real

phi = @(z) tanh(z);
phi_dash = @(z) 1 - tanh(z)^2;

x = [y; z1; z2];
u = r;

z = w1*z1 + w2*z2 + w3*y;

f_x = [
    -y + phi(z) + r;
    -10*z1 + 10*y;
    -100*z2 + 100*y
];

A_x = jacobian(f_x, x);

phi_dash_z = phi_dash(z);
A_x = subs(A_x, diff(phi(z), 1), phi_dash_z);

B = [1; 0; 0]; 

C = [1, 0, 0];

disp('Jacobian matrix A(x):');
disp(A_x);

disp('Input matrix B:');
disp(B);

disp('Output matrix C:');
disp(C);