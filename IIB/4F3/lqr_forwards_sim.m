function [xlog,ulog] = lqr_forwards_sim(A, B, R, x0, Xlog, dt, trange)

iR = inv(R);

xlog = NaN(size(A,1),numel(trange));
ulog = NaN(1,numel(trange)-1);
idx = 1;
x =x0;
xlog(:,idx) = x;
for k1 = trange(1:end-1)
    X = Xlog(:,:,idx);      % Isolate current value of X
    u = -iR*B'*X*x;         % Compute control input
    
    ulog(:,idx) = u;        % Log the control input for plotting
    idx = idx+1;            % Increment counter
    
    dx = (A*x + B*u)*dt;    % Compute state increment
    x = x+dx;               % Update state
    
    xlog(:,idx) = x;        % Log state for plotting
    
end

