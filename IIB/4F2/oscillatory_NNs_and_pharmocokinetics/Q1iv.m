% a) show 0-passive with excess of output passivity

s = tf('s');

m = 0.001;
cv = 0.1;
cp = 2; % \pm 0.1

cp1 = 1.9; cp2 = 2.1;

A1 = [0, 1; -cp1/m, -cv/m];
A2 = [0, 1; -cp2/m, -cv/m];
B = [0; 1/m];
C = [30, 1];
D = 0;


lamda = 20;

cvx_begin sdp
    variable P(2,2) symmetric
            
    LMI1 = [A1'*P + P*A1 + 2*lamda*P, P*B-C';
            B'*P-C, 0] <= 0;
    
    LMI1 = [A2'*P + P*A2 + 2*lamda*P, P*B-C';
            B'*P-C, 0] <= 0;
cvx_end

betaa = 0;

cvx_begin sdp
    variable P(2,2) symmetric
    variable alph
    %variable betaa
    variable epsilon

    minimize(epsilon)
    %minimize(alph)

    LMI1 = alph >= 0;

    LMI2 = epsilon >= 0;
            
    LMI3 = [A1'*P + P*A1 + 2*lamda*P - alph*(C')*C + epsilon*eye(2), P*B-C';
            B'*P-C, -betaa*eye(1)] <= 0;

    LMI4 = [A2'*P + P*A2 + 2*lamda*P - alph*(C')*C + epsilon*eye(2), P*B-C';
            B'*P-C, -betaa*eye(1)] <= 0;
  
cvx_end


% design w for shortage of exactly alpha, the excess of whats being driven
% also enforce 2 passivity

df = [-10, 0, 10;
      0, -100, 100;
      0, 0, -1];
Bu = [0; 0; 1];
Bw = [0; 0; 1];
C = [0, 0, -1]; % ITS 2 PASSIVITY FROM r to -y
Dw = 0;
Du = 0;

n = 3;

betaa2 = alph;

cvx_begin sdp
    variable Y(n,n) symmetric
    variable Z(1,n)
    variable epsilon
    %variable betaa2

    minimize(epsilon)

    LMI1 = epsilon >= 0;
    
    LMI2 = [ (Y*df' + df*Y + 2*lamda*Y + Z'*Bu' + Bu*Z + epsilon*eye(n)),   (Bw - Y*C');
               (Bw' - C*Y),                                (-(Dw + Dw') - betaa2*eye(1))] <= 0;
        
    LMI3 = [ (Y*df' + df*Y + 2*lamda*Y + epsilon*eye(n)),   (Bw - Y*C');
               (Bw' - C*Y),                                (-(Dw + Dw') - betaa2*eye(1))] <= 0;
     
    LMI4 = Y*df' + df*Y + Z'*Bu'+Bu*Z + epsilon*eye(3) <= 0;

    %LMI5 = betaa2 >= alph;

cvx_end

K = Z / Y;

K

figure;
simulate_nonlinear_step(K(1), K(2), K(3), 1e-9);
