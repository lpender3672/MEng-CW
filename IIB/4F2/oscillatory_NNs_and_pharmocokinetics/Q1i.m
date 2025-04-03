close all;

As = [-10, 0; 0, -100];
Bs = [10; 100];
Cs = [1, 0; 0, 1; 0, 0];
Ds = [0; 0; 1];

Gsubs = ss(As, Bs, Cs, Ds);
s = tf('s');

G = Gsubs * 1/(s+1);

G

gama = 2;
lamda = 0.1;

df =[-10, 0, 10; 0, -100, 100; 0, 0, -1];
Bu = [0; 0; 1];
Bw = [0; 0; 1];
C = [0, 0, 1];
Dw = [0];


cvx_begin sdp
    variable Y(3,3) symmetric
    variable Z(1,3)
    variable epsl
    
    minimise(epsl)

    LMI1 = Y >= 0;
    LMI2 = epsl >= 0;
    
    % gain LMI
    LMI3 = [ Y*df'+df*Y + 2*lamda*Y + epsl*eye(3), Bw, Y*C';
             Bw', -gama*eye(1), Dw';
             C*Y, Dw, -gama*eye(1) ] <= 0;
    
    LMI4 = [ Y*df'+df*Y + 2*lamda*Y + epsl*eye(3) + Z'*Bu' + Bu*Z, Bw, Y*C';
             Bw', -gama*eye(1), Dw';
             C*Y, Dw, -gama*eye(1) ] <= 0;
         
cvx_end

K = Z * inv(Y)


w1 = K(1);
w2 = K(2);
w3 = K(3);

figure;
hold on;
simulate_nonlinear_step(w1, w2, w3, -1);
simulate_nonlinear_step(w1, w2, w3, 0);
simulate_nonlinear_step(w1, w2, w3, 1);
hold off;
legend('r=-1', 'r=0', 'r=1', 'Location', 'best')

print(gcf, 'figures/11_step_reference.png', '-dpng', '-r600');

figure;
hold on;
simulate_nonlinear_harmonic(w1, w2, w3, 1, pi, 0);
simulate_nonlinear_harmonic(w1, w2, w3, 1, pi/2, 0);
%t = linspace(0, 10, 100);
%plot(t, sin(pi * t))
hold off;
ylabel('Signal Amplitude')
legend('r=sin(\pi t)', 'r=sin(\pi/2 t)')
print(gcf, 'figures/11_harmonic_reference.png', '-dpng', '-r600');


%% now for differential

% constnt

dxes = linspace(-5, 5, 100);
c_gammas = zeros(size(dxes));

for i = 1:size(dxes, 2) 
    x1 = 1.0;
    x2 = dxes(i) * x1;
    
    [t, y1, y2] = simulate_nonlinear_dstep(w1, w2, w3, x1, x2);
    
    edx = trapz(t, abs(x1-x2).^2 * ones(size(t)));
    edy = trapz(t, abs(y1-y2).^2);

    c_gammas(i) = edy / edx;

end

figure;
plot(dxes, c_gammas)
ylabel('E(y_1 - y_2)/E(r_1 - r_2)')
xlabel('r_2 / r_1')
grid on;
print(gcf, 'figures/11_step_incremental_gain.png', '-dpng', '-r600');

% harmonic

damps = linspace(-5, 5, 100);
h_gammas = zeros(size(damps));

for i = 1:size(damps, 2) 
    A1 = 1.0;
    A2 = damps(i) * A1;
    
    [t, y1, y2] = simulate_nonlinear_dharmonic(w1, w2, w3, A1, A2);

    r1 = A1 * sin(pi * t );
    r2 = A2 * sin(pi * t );
    
    edx = trapz(t, abs(r1-r2).^2);
    edy = trapz(t, abs(y1-y2).^2);

    h_gammas(i) = edy / edx;

end

figure;
plot(damps, h_gammas)
ylabel('E(y_1 - y_2)/E(r_1 - r_2)')
xlabel('r_2 / r_1')
grid on;
print(gcf, 'figures/11_harmonic_incremental_gain.png', '-dpng', '-r600');


%{

for w1 = [0.1:0.1:0.1]
    for w2 = [0.1:0.1:0.1]
        
        N = [zeros(2,3); w1, w2, w3];

        cvx_begin sdp
            variable P(n,n) symmetric

            LMI1 = P >= 0
            % gain LMI
            LMI2 = [ A0'*P + P*A0 + 2*lamda*P + 1/gama * C'*C, P*B;
                    B'*P, -gama * eye(1)] <= 0;

            LMI3 = [(A0+N)'*P + P*(A0+N) + 2*lamda*P + 1/gama * C'*C, P*B;
                    B'*P, -gama*eye(1)] <= 0;

        cvx_end

        if strcmp(cvx_status, 'Solved')
                fprintf('Feasible solution found for w1 = %.2f\n', w1);
                break
        else
                fprintf('No solution for w1 = %.2f, status: %s\n', w1, cvx_status);
        end
    end
end
%}
