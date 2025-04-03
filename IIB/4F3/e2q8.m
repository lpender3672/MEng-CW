

AplusBKrhs = [0.7619, 0.4762; -0.4762, -0.0476];

x0 = [3.4; 1.7];

Nsim = 30;

X = zeros(2, Nsim+1);
X(:,1) = x0;

% Simulate:
for k = 1:Nsim
    X(:, k+1) = AplusBKrhs * X(:, k);
end

figure;
hold on;
plot(X(1,:));
plot(X(2,:));

A = [1 ,1; 0, 1];  % Fill in your A
B = [0.5; 1];  % Fill in your B

% Cost function weights:
Q = eye(2);  % e.g. eye(2)
R = eye(2);  % e.g. 1 or eye(1)
P = 2 * eye(2);


X_con = zeros(2, Nsim+1);
X_con(:,1) = x;

for k = 1:Nsim

    
    
    [z_opt, ~, exitflag] = quadprog(H, f, Aineq, bineq, Aeq, beq, lb, ub, [], options);
    
    if exitflag < 1
       warning('QP did not converge at step %d. Using zero control.', k);
       u_opt = 0;
    else

       % if the first element of z is u(0)
       u_opt = z_opt(1);  
    end
    
    x = A*x + B*u_opt;
    X_con(:, k+1) = x;
end