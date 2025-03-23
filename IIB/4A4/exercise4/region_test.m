%clear; clc; close all;

G = tf([-2.637 -2.475 -0.0607, 0], longitudinal_den);
figure('Color','w'); 
rlocus(G);
title('Root Locus with Damping Ratio and Natural Frequency Constraints');
grid on; hold on;
axis([-5 2 -5 5]);  % Adjust as needed

[xgrid, ygrid] = meshgrid(linspace(-5,0,400), linspace(-5,5,400));
sigma = xgrid;        % real part
omega = ygrid;        % imaginary part

r = sqrt(sigma.^2 + omega.^2); 
validPoints = (r > 1e-8);

zeta_grid = zeros(size(r));
zeta_grid(validPoints) = -sigma(validPoints) ./ r(validPoints);

regionMask = (sigma < 0) & (zeta_grid < 0.2);

p = pcolor(xgrid, ygrid, double(regionMask));
set(p, 'EdgeColor', 'none', 'FaceAlpha', 0.2, 'FaceColor','r');
shading flat;

zeta_boundary = 0.2;
omega_n_vec = linspace(0,5,300);  % adjust as needed
sigma_vec = -zeta_boundary * omega_n_vec; 
omega_vec = omega_n_vec * sqrt(1 - zeta_boundary^2);

theta = linspace(0, 2*pi, 200);
circle_x = cos(theta);
circle_y = sin(theta);
patch(circle_x, circle_y, 'r', 'FaceAlpha', 0.05, 'EdgeColor', 'none');
text(0.7, 0.1, '\omega_n = 1', 'Color','r','FontWeight','bold');

xlabel('Real Axis (Re(s))');
ylabel('Imag Axis (Im(s))');
legend('Root Locus','Region: ζ < 0.2','\zeta=0.2 boundary','Region: \omega_n < 1','Location','Best');


%stepinfo(feedback(G*k_vals(i), 1));
%rise_time = step_response.RiseTime
%settle_times(i) = step_response.RiseTime;
%peak_time = step_response.PeakTime
%overshoot = step_response.Overshoot
    