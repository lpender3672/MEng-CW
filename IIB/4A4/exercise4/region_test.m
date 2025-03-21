%clear; clc; close all;

%% 1) Define a sample transfer function for demonstration
%    For instance: G(s) = (s+3)/(s*(s+2)*(s+1))

G = tf([-2.637 -2.475 -0.0607, 0], longitudinal_den);
figure('Color','w'); 
rlocus(G);
title('Root Locus with Damping Ratio and Natural Frequency Constraints');
grid on; hold on;
axis([-5 2 -5 5]);  % Adjust as needed

%% 3) Shade the region where damping ratio ζ < 0.2
%    Create a grid over the s-plane (for the stable region: sigma < 0)
[xgrid, ygrid] = meshgrid(linspace(-5,0,400), linspace(-5,5,400));
sigma = xgrid;        % real part
omega = ygrid;        % imaginary part

% Compute the magnitude r = sqrt(sigma^2 + omega^2) (avoid division by zero)
r = sqrt(sigma.^2 + omega.^2); 
validPoints = (r > 1e-8);

% Damping ratio for stable poles (sigma < 0):
%    ζ = -sigma / sqrt(sigma^2 + omega^2)
zeta_grid = zeros(size(r));
zeta_grid(validPoints) = -sigma(validPoints) ./ r(validPoints);

% Create a mask for points with sigma < 0 and ζ < 0.2
regionMask = (sigma < 0) & (zeta_grid < 0.2);

% Use pcolor to shade the region (convert logical to double)
p = pcolor(xgrid, ygrid, double(regionMask));
set(p, 'EdgeColor', 'none', 'FaceAlpha', 0.2, 'FaceColor','r');
shading flat;

%% 4) Overlay the boundary line for ζ = 0.2
%    For a given ζ, the pole location in the s-plane can be parameterized as:
%       σ = -ζ*ω_n,   ω = ω_n*sqrt(1-ζ²)
zeta_boundary = 0.2;
omega_n_vec = linspace(0,5,300);  % adjust as needed
sigma_vec = -zeta_boundary * omega_n_vec; 
omega_vec = omega_n_vec * sqrt(1 - zeta_boundary^2);

%% 5) Add a circle patch for the natural frequency requirement ωₙ > 1
%    The natural frequency is ωₙ = sqrt(σ² + ω²). Thus, the region with ωₙ < 1
%    is the interior of a circle of radius 1 centered at the origin.
theta = linspace(0, 2*pi, 200);
circle_x = cos(theta);
circle_y = sin(theta);
patch(circle_x, circle_y, 'r', 'FaceAlpha', 0.05, 'EdgeColor', 'none');
% Label the circle boundary
text(0.7, 0.1, '\omega_n = 1', 'Color','r','FontWeight','bold');

%% Final touches
xlabel('Real Axis (Re(s))');
ylabel('Imag Axis (Im(s))');
legend('Root Locus','Region: ζ < 0.2','\zeta=0.2 boundary','Region: \omega_n < 1','Location','Best');


%stepinfo(feedback(G*k_vals(i), 1));
%rise_time = step_response.RiseTime
%settle_times(i) = step_response.RiseTime;
%peak_time = step_response.PeakTime
%overshoot = step_response.Overshoot
    