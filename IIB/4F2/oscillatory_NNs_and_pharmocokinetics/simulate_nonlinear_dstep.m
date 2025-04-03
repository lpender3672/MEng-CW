

function [t, y1_out, y2_out] = simulate_nonlinear_dstep(w1, w2, w3, r1, r2)
    
    tspan = [0 20];
    x0 = [0; 0; 0];

    t = linspace(tspan(1), tspan(2), 500);

    [~, x1] = ode45(@(t,x) q1ode(t, x, r1, w1, w2, w3), t, x0);
    [~, x2] = ode45(@(t,x) q1ode(t, x, r2, w1, w2, w3), t, x0);
    
    y1_out = x1(:,3);
    y2_out = x2(:,3);
    
    dr = (r1 - r2) * ones(size(t));

    if nargout > 0
        return;
    end

    hold on;
    plot(t, dr);
    plot(t, y1_out - y2_out);
    hold off;

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