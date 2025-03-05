
% SS


E1 = [1, 0, 0, 0, 0, 0;
     0, 1, 0, 0, 0, 0;
     0, 0, 1, 0, 0, -tau^2;
     0, 0, 0, 1, -tau^2, 0;
     0, 0, 0, -1/tau^2, 1, 0;
     0, 0, -1/tau^2, 0, 0, 1]

A1 = [0, 0, 0, 1, 0, 0;
      0, 0, 0, 0, 0, 1;
      0, 1, 0, 0, 0, 2*tau;
      0, 1, 0, 0, 2*tau, 0;
      0, -1/tau^2, 0, 0, -2/tau, 0;
      0, -1/tau^2, 0, 0, 0, -2/tau]

B1 = [0, 0, 0, 0;
      0, 0 ,0 ,0;
      0, 1, 1, 0;
      0, 1, 0, 1;
      0, -1/tau^2, 0, -1/tau^2;
      0, -1/tau^2, -1/tau^2, 0]

L = [0, 1, 0, 0;
     0, 0, 1, 0;
     0, 0, 0, 1;
     -16, -32, -24, -8]

A2 = [L, zeros(4);
      zeros(4), L]

zr4 = zeros(1,4);
B2 = [zr4; zr4; zr4;
      16, 0, 0, 0;
      zr4; zr4; zr4;
      0, 16, 0, 0]

zr6 = zeros(1,6);

W = [zr6; zr6; zr6;
    -16, 0, zr4;
    zr6; zr6; zr6;
    0, 16, zr4]

Ap = [A1, zeros(6, 8);
     W, A2]

Bp = [B1;
     B2]

E = [E1, zeros(6,8);
    zeros(8,6), eye(8)]

% this is zero which doesnt seem good
det(E)

% continue on to get C and D
C = [0, 1, zr6, zr6;
     1, 0, zr6, zr6;
     zr6, 1, 0, zr6;
     zr6, zr4, 1, 0, 0, 0]
D = 0