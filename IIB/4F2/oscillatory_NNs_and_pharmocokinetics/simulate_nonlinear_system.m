

function simulate_nonlinear_system(w1, w2, w3)
    
    tspan = [0 10];
    x0 = [0; 0; 0];

    [t, x] = ode45(@(t,x) q1ode(t, x, w1, w2, w3), tspan, x0);
    
    y_out = x(:,3);
    
    figure;
    plot(t, y_out, 'LineWidth', 2);
    xlabel('Time (s)');
    ylabel('y(t)');
    grid on;
end

function dxdt = q1ode(t, x, w1, w2, w3)
    % x(1) = z1, x(2) = z2, x(3) = y
    z1 = x(1);
    z2 = x(2);
    y  = x(3);
    
    r = 1;
    
    nonlinear_arg = w1*z1 + w2*z2 + w3*y;
    
    dz1dt = -z1 + y;
    dz2dt = -z2 + y;
    dydt  = -y + r + tanh(nonlinear_arg);
    
    dxdt = [dz1dt; dz2dt; dydt];
end