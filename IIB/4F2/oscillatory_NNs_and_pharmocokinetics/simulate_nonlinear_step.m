

function [t, y_out] = simulate_nonlinear_step(w1, w2, w3, r)

    if nargin < 4
        r = 1;
    end
    
    tspan = [0 50];
    x0 = [0; 0; 0];

    [t, x] = ode45(@(t,x) q1ode(t, x, r, w1, w2, w3), tspan, x0);
    
    y_out = x(:,3);
    
    plot(t, y_out);
    xlabel('Time (s)');
    ylabel('y(t)');
    grid on;
end

function dxdt = q1ode(t, x, r, w1, w2, w3)
    % x(1) = z1, x(2) = z2, x(3) = y
    z1 = x(1);
    z2 = x(2);
    y  = x(3);
    
    %r = 1;
    
    nonlinear_arg = w1*z1 + w2*z2 + w3*y;
    
    dz1dt = -z1 + y;
    dz2dt = -z2 + y;
    dydt  = -y + r + tanh(nonlinear_arg);
    
    dxdt = [dz1dt; dz2dt; dydt];
end