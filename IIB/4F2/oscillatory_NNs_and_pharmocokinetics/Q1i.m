
As = [-10, 0; 0, -100];
Bs = [10; 100];
Cs = [1, 0; 0, 1; 0, 0];
Ds = [0; 0; 1];

Gsubs = ss(As, Bs, Cs, Ds);
s = tf('s');

G = Gsubs * 1/(s+1);

G

w1 = 1.0;
w2 = 1.0;
w3 = 1.0;

A0 =[-1, 0, 0; 10, -10, 0; 100, 0, -100];
N = [w3, w1, w2; zeros(2,3)];
B = [1; 0; 0];
C = [1, 0, 0];


simulate_nonlinear_system(w1, w2, w3);

n = size(A0, 1)
m = size(B, 2)

cvx_begin sdp
    variable Y(n,n) symmetric
    variable Z(m,n)
    variable epsilon
    variable gama
    
    %minimise(gama)
    minimise(epsilon) % otherwise makes very high

    LMI1 = Y >= 0
    LMI2 = gama <= 0.1
    
    % gain LMI
    %
    LMI3 = [ (Y*A' + A*Y + Z'*Bu' + Bu*Z),   (Y*Cz' + Z'*Dzu'),          Bw;
            (Cz*Y + Dzu*Z),  -gama*eye(2),      Dzw';
            Bw',            Dzw,                -gama*eye(2) ] <= 0;
    
cvx_end