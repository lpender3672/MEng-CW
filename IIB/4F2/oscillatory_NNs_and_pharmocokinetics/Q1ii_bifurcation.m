
close all;

phi = @(u) tanh(u);
phi_prime = @(u) 1 - tanh(u).^2;

w3_left = -100:2:-24;
w3_mid = -24:0.01:-22;
w3_right = -22:2:100;

w3_vals = [w3_left, w3_mid, w3_right]

% cells because unknown number of equilibria solns
equilibria = cell(length(w3_vals), 1);
stability = cell(length(w3_vals), 1);

options = optimset('Display','off','TolFun',1e-8);

y_initials = linspace(-1, 1, 5);

% Loop over each w3 value
for i = 1:length(w3_vals)
    w3 = w3_vals(i);
    sol_set = [];
    stab_set = [];

    f = @(y) y - phi((w3 + 25)*y);
    for y0 = y_initials
        [y_sol, ~, exitflag] = fsolve(f, y0, options);
        if exitflag > 0

            if isempty(sol_set) || all(abs(sol_set - y_sol) > 1e-3)
                sol_set(end+1) = y_sol;
                
                % eigenvalues of jacobian computed at equilibria point
                u = (w3+25)*y_sol;
                a11 = -1 + 25*phi_prime(u);
                a12 = w3 * phi_prime(u);
                J = [a11, a12; 10, -10];
                e_vals = eig(J);
                
                if (all(real(e_vals) < 0))
                    stab_set(end+1) = 1;  % stable node or inward spiral
                elseif (all(real(e_vals) > 0))
                    stab_set(end+1) = 2;  % fully unstable node or outward spiral
                else
                    stab_set(end+1) = 3;  % saddle point?
                    display('SADDLE!!!')
                end
            end
        end
    end
    equilibria{i} = sol_set;
    stability{i} = stab_set;
end

    figure; hold on; grid on;
h_stable = []; h_unstable = []; h_saddle = [];

for i = 1:length(w3_vals)
    w3 = w3_vals(i);
    eq_points = equilibria{i};
    stab_points = stability{i};
    for j = 1:length(eq_points)
        if stab_points(j) == 1
            % legends in matlab are fucking stupid
            if isempty(h_stable)
                h_stable = plot(w3, eq_points(j), 'go', 'MarkerFaceColor', 'g', 'MarkerSize', 2);
            else
                plot(w3, eq_points(j), 'go', 'MarkerFaceColor', 'g', 'MarkerSize', 2);
            end
        elseif stab_points(j) == 2
            if isempty(h_unstable)
                h_unstable = plot(w3, eq_points(j), 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 2);
            else
                plot(w3, eq_points(j), 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 2);
            end
        else
            if isempty(h_saddle)
                h_saddle = plot(w3, eq_points(j), 'bo', 'MarkerFaceColor', 'b', 'MarkerSize', 2);
            else
                plot(w3, eq_points(j), 'bo', 'MarkerFaceColor', 'b', 'MarkerSize', 2);
            end
        end
    end
end

xlabel('w_3');
ylabel('Equilibrium y = z_1');
ylim([-1.5, 1.5])
if isempty(h_saddle)
    legend([h_stable, h_unstable], 'Stable Equilibrium', 'Unstable Equilibrium', 'Location', 'Best');
else
    legend([h_stable, h_unstable, h_saddle], 'Stable Equilibrium', 'Unstable Equilibrium', 'Saddle Equilibrium', 'Location', 'Best');
end

print(gcf, 'figures/equilibria_bifurcation.png', '-dpng', '-r600');


