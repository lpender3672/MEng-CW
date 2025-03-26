
close all;

df = [-10, 0, 10;
      0, -100, 100;
      0, 0, -1];
Bu = [0; 0; 1];
Bw = [0; 0; 1];
Dw = 0;
Du = 0;


lamda = 20;

n=3;

cvx_begin sdp
            variable Y(n,n) symmetric
            variable Z(1,n)
            variable epsilon
            
            minimize( eps )
            
            LMI1 = epsilon >= 0;
                                                % gain LMI
            LMI2 = df*Y + Y*df' + 2*lamda*Y + Z'*Bu' + Bu*Z + eps*eye(n) <= 0;
            LMI3 = df*Y + Y*df' + 2*lamda*Y + eps*eye(n) <= 0;
            
            LMI4 = [Y*df' + df*Y + Z'*Bu'+Bu*Z+eps*eye(3)] <= 0;
            
            %LMI4 = trace(Y) <= 0;
            
cvx_end


if strcmp(cvx_status, 'Solved')
    p = sum(eig(Y) < -1e-10);
end
K = Z / Y;

disp(K)

simulate_nonlinear_step(K(1), K(2), K(3));
print(gcf, 'figures/13_oscillator_responses.png', '-dpng', '-r600');

