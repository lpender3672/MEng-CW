

function [t, y_out] = Pharmacokinetic_sim(k, r)

    tau = 0.1;
    
    history = @(t) [0; 0; 0];
    
    sol = dde23(@(t,x,Z) q2dde(t,x,Z,k,r), ...
                tau, ...               % delay
                history, ...           % initial function
                [0, 30]);
    
    % Extract solution
    t = sol.x;
    y_out = sol.y;

    plot(t, y_out(1,:))
    grid on;

end


function dxdt = q2dde(t, x, Z, k, r) 
    alpha12 = 0.1;
    alpha21 = 0.05;
    % x(1) = z1, x(2) = z2, x(3) = y
    c1     = x(1);
    c2     = x(2);
    x3     = x(3);

    xDelayed = Z(:,1);
    x3_del    = xDelayed(3);

    %u = k * relu(r - x3_del);
    u = k * max(0, r - x3_del);

    dc1dt = -0.01*c1 - alpha12*c1 + alpha21*c2 + u;
    dc2dt = -0.01*c2 - alpha21*c2 + alpha12*c1;
    dx3dt = ( -x3 + c1 ) / 10;   % same as before

    dxdt = [dc1dt; dc2dt; dx3dt];
end