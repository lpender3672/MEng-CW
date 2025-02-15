function [A, B, C, D, G] = nominal()
% functionmake control system
% nyquist 

m = 1.0;
cv = 1.0;
cp = 1.0;

% state matricies

A = [0, 1; -cp/m, -cv/m];
B = [0; cp/m];
C = [1, 0];
D = 0;

G = ss(A,B,C,D);

end