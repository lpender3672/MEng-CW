

function [t, y1_out, y2_out] = simulate_nonlinear_dharmonic(w1, w2, w3, mag1, mag2, freq1, freq2, phase1, phase2)

    if nargin < 8
        phase1 = 0;
        phase2 = 0;
    end
    if nargin < 6
        freq1 = pi;
        freq2 = pi;
    end
    
    tspan = [0 10];
    x0 = [0; 0; 0];

    t = linspace(tspan(1), tspan(2), 500);

    [~, x1] = ode45(@(t,x) q1ode(t, x, w1, w2, w3, mag1, freq1, phase1), t, x0);
    [~, x2] = ode45(@(t,x) q1ode(t, x, w1, w2, w3, mag2, freq2, phase2), t, x0);
    
    y1_out = x1(:,3);
    y2_out = x2(:,3);

    if nargout > 0
        return;
    end

    r1 = mag1 * sin(freq1 * t + phase1);
    r2 = mag2 * sin(freq2 * t + phase2);
    
    hold on;
    plot(t, r1 - r2);
    plot(t, y1_out - y2_out);
    hold off;

    xlabel('Time (s)');
    ylabel('y(t)');
    grid on;
end

function dxdt = q1ode(t, x, w1, w2, w3, mag, freq, phase)
    % x(1) = z1, x(2) = z2, x(3) = y
    z1 = x(1);
    z2 = x(2);
    y  = x(3);
    
    r = mag * sin(freq * t + phase);
    
    nonlinear_arg = w1*z1 + w2*z2 + w3*y;
    
    dz1dt = -z1 + y;
    dz2dt = -z2 + y;
    dydt  = -y + r + tanh(nonlinear_arg);
    
    dxdt = [dz1dt; dz2dt; dydt];
end