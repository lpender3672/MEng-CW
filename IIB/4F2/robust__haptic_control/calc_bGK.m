function bGK = calc_bGK(G, K)
    % Ensure G and K are state-space models
    G = ss(G);
    K = ss(K);
    
    I_sys = eye(size(G,1));
    
    try
        inv_term = inv(I_sys - G*K); % Compute (I - GK)^(-1)
    catch
        warning('System is unstable or singular, returning bGK = 0');
        bGK = 0;
        return;
    end

    M = [K; I_sys] * inv_term * [I_sys, G];

    norm_M = norm(M, inf);

    bGK = 1 / norm_M;
    
    fprintf('Computed b(G, K) = %.4f\n', bGK);
end