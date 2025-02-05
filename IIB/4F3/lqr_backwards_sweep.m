function Xlog = lqr_backwards_sweep(A, B, Q, R, XN, dt, trange)
% 

% Compute inverse of R since we use it a lot
iR = inv(R);

% Integrate backwards and store the result
trange_reverse = trange(end:-1:1);
Xlog = NaN(size(A,1),size(A,2),numel(trange_reverse));
idx = numel(trange_reverse);
Xlog(:,:,end) = XN;
X = XN;
for k1 = trange_reverse(1:end-1)
    idx = idx-1;
    Xdot = -(Q + X*A + A'*X - X*B*iR*B'*X);
    X = X - Xdot*dt;
    Xlog(:,:,idx) = X;
end
